# -*- coding: utf-8 -*-
"""
Created on Mon May 29 21:50:56 2017

@author: erwan

A Spectrum Database class to manage them all

It basically manages a list of Spectrum JSON files, adding a Pandas
dataframe structure on top to serve as an efficient index to visualize
the spectra input conditions, and slice through the Dataframe with
easy queries

Example
-------

    >>> from neq.spec import SpecDatabase
    >>> db = SpecDatabase(r"path/to/database")     # create or loads database

    >>> db.update()  # in case something changed (like a file was added manually)
    >>> db.see(['Tvib', 'Trot'])   # nice print in console

    >>> s = db.get('Tvib==3000 & Trot==1500')[0]  # get all spectra that fit conditions
    >>> db.add(s)  # update database (and raise error because duplicate!)

Note that SpectrumFactory objects can be configured to automatically update
a database

Edit database: 
    
An example of script to update all spectra conditions in a database (ex: when 
a condition was added afterwards to the Spectrum class)
    
    >>> # Example: add the 'medium' key in conditions 
    >>> db = "database_CO"
    >>> for f in os.listdir(db):
    >>>    if not f.endswith('.spec'): continue
    >>>    s = load_spec(join(db, f))
    >>>    s.conditions['medium'] = 'vacuum'
    >>>    s.store(join(db,f), if_exists_then='replace')

Todo
----

Alert if case already in database when generating from a SpectrumFactory / ParallelFactory
connected to a SpecDatabase

Implement a h5py version of load / store 

"""

from __future__ import absolute_import
from __future__ import print_function
import json
import numpy as np
from numpy import array
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os
import sys
from warnings import warn
from os.path import (join, splitext, exists, basename, split, dirname, abspath, 
                     isdir, getsize)
from six.moves import range
from radis.spectrum.spectrum import Spectrum, is_spectrum
from shutil import copy2
from time import strftime
from radis.misc.basics import is_float, list_if_float
from radis.misc.utils import FileNotFoundError, PermissionError
from radis.misc.debug import printdbg
from six import string_types


# Serializing functions
# ... functions to store / load a Spectrum to / from a JSON file

# %% Save functions

def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False
    
def save(s, path, discard=[], compress=False, add_info=None, add_date=None, 
         if_exists_then='increment', verbose=True, warnings=True):
    ''' Save a Spectrum object in JSON format. Object can be recovered with 
    radis.tools.load_spec()
    
    Parameters
    ----------

    s: Spectrum
        to save

    path: str
        filename to save. No extension needed. If filename already
        exists then a digit is added. If filename is a directory then a new
        file is created within this directory.

    discard: list of str
        parameters to discard. To save some memory.
        
    compress: boolean
        if True, removes all quantities that can be regenerated with s.update(),
        e.g, transmittance if abscoeff and path length are given, radiance if
        emisscoeff and abscoeff are given in non-optically thin case, etc.
        Default False

    add_info: list, or None/False
        append these parameters and their values if they are in conditions.
        e.g:
        >>> add_info = ['Tvib', 'Trot']

    add_date: str, or None/False
        adds date in strftime format to the beginning of the filename.
        e.g:
        >>> add_date = '%Y%m%d'
        Default ''

    if_exists_then: 'increment', 'replace', 'error'
        what to do if file already exists. If increment an incremental digit
        is added. If replace file is replaced (yeah). If error (or anything else)
        an error is raised. Default `increment`

    Returns
    -------

    Returns filename used (may be different from given path as new info or
    incremental identifiers are added)

    '''

    # 1) Format to JSON writable dictionary
    sjson = _format_to_jsondict(s, discard, compress, verbose=verbose)

    # 2) Get final output name (add info, extension, increment number if needed)
    fout = _get_fout_name(path, if_exists_then, add_date, add_info, 
                          sjson, verbose)
    
    # 3) Now is time to save
    with open(fout, 'w') as f:
        try:
            json.dump(sjson, f)
        except TypeError:
            _export_safe(sjson, f, warnings=warnings)
    if verbose: print('Spectrum stored in {0} ({1:.1f}Mb)'.format(fout,
                       getsize(fout)/1024*1e-3))

    return fout    # return final name

def _format_to_jsondict(s, discard, compress, verbose=True):
    ''' Format to JSON writable dictionary 
    
    Notes
    -----
    
    path names create much troubles on reload if they are stored with '/' 
    Make sure we use raw format 
    '''
    
    # ... add main attributes from Spectrum class
    sjson = {}
    sjson['q'] = {}
    sjson['q_conv'] = {}
    for k, v in s._q.items():
        sjson['q'][k] = v.tolist()
    for k, v in s._q_conv.items():
        sjson['q_conv'][k] = v.tolist()
        
    if compress:
        sjson = _compress(s, sjson) #, s.conditions, equilibrium=s.is_at_equilibrium())
    
    # ... Format conditions, check that minimum information is given
    try:
        conditions = s.conditions
    except AttributeError:
        raise ValueError('Spectrum needs a `conditions` attribute (dict) to be stored in database')
    try:
        conditions['waveunit']
    except KeyError:
        raise KeyError('Spectrum `conditions` dict should at least have a `waveunit` key')
    # Todo: what if conditions is an empty dictionary? do we allow that?
    # ... now let's store all conditions
    sjson['conditions'] = {}
    for k, v in conditions.items():
        # If it looks like string, store as raw text (that fixes most trouble with paths)
        if type(v) in string_types:
            sjson['conditions'][k] = r'{0}'.format(v)
        else:
            # Store the object directly
            if is_jsonable(v):
                sjson['conditions'][k] = v
            else:
                if verbose:
                    print('condition {0}, type {1} not jsonable and discarded'.format(
                            k, type(v)))
            
    # ... Only `quantities` and `conditions` are required. The rest is just extra
    # details. Add them now if they exist (assuming a Spectrum class is being stored)
    for attr in ['units', 'cond_units', 'name']:
        if attr not in discard:
            try:
                sjson[attr] = s.__getattribute__(attr)
            except AttributeError:
                pass
    # ... special case of slit (a dictionary of arrays)
    if '_slit' not in discard:
        sjson['slit'] = {}
        for k, v in s._slit.items():
            sjson['slit'][k] = v.tolist()
    # ... special case of lines (a Pandas dataframe): 
    if 'lines' not in discard:
        try:
            if s.lines is not None:
                sjson['lines'] = s.lines.to_json()   # Pandas > JSON conversion
                sjson['_dtypes_lines'] = s.lines.dtypes.to_json()  # Keep dtype 
        except AttributeError:
            pass  # dont store lines if they dont exist
    # ... special case of populations (a dict of dict of dict of Pandas dataframes)
    if 'populations' not in discard:
        try:
            if s.populations is not None:
                pops = s.populations
                jsonpops = {}
                for molecule, isotopes in pops.items():
                    jsonpops[molecule] = {}
                    for isotope, elec_states in isotopes.items():
                        jsonpops[molecule][isotope] = {}
                        for elec_state, content in elec_states.items():
                            jsonpops[molecule][isotope][elec_state] = {}
                            for k, v in content.items():
                                if isinstance(v, pd.DataFrame): # rovib or vib levels
                                    vjson = v.to_json()   # Pandas > JSON conversion
                                    jsonpops[molecule][isotope][elec_state][k] = vjson
                                    jsonpops[molecule][isotope][elec_state]['_dtypes_'+k] = v.dtypes.to_json()
                                else:   # can be other data. Hopefully serializable. 
                                    vjson = v
                                    jsonpops[molecule][isotope][elec_state][k] = vjson
            sjson['populations'] = jsonpops
        except AttributeError:
            pass  # dont store populations if they dont exist
    
    return sjson

def _get_fout_name(path, if_exists_then, add_date, add_info, sjson, verbose):
    ''' Get final output name   (add info, extension, increment number if needed) '''
    
    conditions = sjson['conditions']
    
    if isdir(path):
        fold, name = path, ''
    else:
        fold, name = split(path)

    # ... add date info
    if add_date not in ['', None, False]:
        date = strftime(add_date)
    else:
        date = ''

    # ... add conditions info
    if add_info not in [[], {}, None, False]:
        # complete name with info about calculation conditions
        info = []
        for k in add_info:
            if k in conditions:
                v = conditions[k]
                # Format info
                # ... special cases
                if k in ['Tvib', 'Tgas', 'Trot']:
                    vs = "{0:.0f}".format(v)
                # ... general case
                elif is_float(v): 
                    vs = "{0:.3g}".format(v)
                else:
                    vs = "{0}".format(v)
                    
                try:
                    un = sjson['cond_units'][k]
                except KeyError: # units not defined, or no units for this condition
                    un = ''
                info.append("{0}{1}{2}".format(k, vs, un))
                # Note: should test for filename validity here.
                # See https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
                # but it looks long. Best is probably to just test write a file
            else:
                if verbose: print(('Warning. {0} not a valid condition'.format(k)))
        info = '_'.join([_f for _f in info if _f])
    else:
        info = ''
        
    # ... clean from forbidden characters
    for c in [r'/']:
        info = info.replace(c, '')

    # ... get extension
    rad, ext = splitext(name)
    if ext == '':
        ext = '.spec'    # default extension

    # ... Write full name
    name = '_'.join([_f for _f in [date,rad,info] if _f])+ext
    fout = join(fold, name)

    # ... Test for existence, replace if needed
    if exists(fout):
        if if_exists_then=='increment':
            if verbose: print('Warning. File already exists. Filename is incremented')
            i = 0
            while exists(fout):
                i += 1
                name = '_'.join([_f for _f in [date,rad,info,str(i)] if _f])+ext
                fout = join(fold, name)
        elif if_exists_then=='replace':
            if verbose: print(('File exists and will be replaced: {0}'.format(name)))
        else:
            raise ValueError('File already exists {0}. Choose another filename'.format(fout)+\
                             ', or set the `if_exists_then` option to `replace` or ìncrement`')

    return fout

def _compress(s, sjson): 
    ''' if True, removes all quantities that can be regenerated with s.update(),
    e.g, transmittance if abscoeff and path length are given, radiance if
    emisscoeff and abscoeff are given in non-optically thin case, etc.
    Default False '''
    
    
    from radis.spectrum.rescale import get_redundant
    redundant = get_redundant(s)
    
    discarded = []
    for key in list(sjson['q'].keys()):
        if key == 'wavespace': continue
        if redundant[key]:
            del sjson['q'][key]
            discarded.append(key)
    for key in list(sjson['q_conv'].keys()):
        if key == 'wavespace': continue
        if redundant[key]:
            del sjson['q_conv'][key]
            discarded.append(key)
        
    if len(discarded)>0:
        print(('Redundant quantities removed: {0}. Use s.update() after '.format(discarded)+\
              'loading to regenerate them'))
    
    return sjson

def _export_safe(sjson, f, warnings=True):
    ''' Export only jsonable attributes in 'conditions' '''
    
    # remove non jsonable objects
    discard = []
    for k,v in sjson['conditions'].items():
        if not is_jsonable(v):
            discard.append(k)
            if warnings: print(("... discard conditions['{0}'] as non jsonable".format(k)))
    new_conds = {k:v for k,v in sjson['conditions'].items() if not k in discard}
    sjson['conditions'] = new_conds  # dont modify initial spectrum
    
    if 'populations' in list(sjson.keys()):
        # remove non jsonable objects
        # (note: Specair generated populations include numpy arrays tht could
        # be jsonized eventually... just look at what's done with quantities... 
        # but for the time being we just discard them)
        discard = []
        for k,v in sjson['populations'].items():
            if not is_jsonable(v):
                discard.append(k)
                if warnings: print(("... discard populations['{0}'] as non jsonable".format(k)))
        new_pops = {k:v for k,v in sjson['populations'].items() if not k in discard}
        sjson['populations'] = new_pops
    
    # retry export
    json.dump(sjson, f)
    
    
# %% Load functions

def load(file):
    '''
    Parameters
    ----------

    file: str
        .spec file to load

    (wrapper to neq.spec.load)

    '''

    warn(DeprecationWarning("load replaced with more explicit load_spec"))

    return load_spec(file)

def load_spec(file):
    '''
    Parameters
    ----------

    file: str
        .spec file to load

    '''

    with open(file, 'r') as f:
        try:
            sload = json.load(f)
        except:
            print(('Error opening file {0}'.format(f)))
            raise

    # Test format / correct deprecated format:
    sload = _fix_format(file, sload)

    # ... Back to real stuff:
    conditions = sload['conditions']
    
    # Get quantities 
    if 'quantities' in sload:
        # old format -saved with tuples (w,I) under 'quantities'): heavier, but 
        # easier to generate a spectrum 
        quantities = {k: (np.array(v[0]), array(v[1]))
                            for (k, v) in sload['quantities'].items()}
        warn("File {0}".format(basename(file))+" has a deprecrated structure ("+\
              "quantities are stored with shared wavespace: uses less space). "+\
            "Regenerate database ASAP.", DeprecationWarning)
    else:
        quantities = {k:(sload['q']['wavespace'],v) for k,v in sload['q'].items() 
                            if k != 'wavespace'}
        quantities.update({k:(sload['q_conv']['wavespace'],v) for k,v in sload['q_conv'].items() 
                            if k != 'wavespace'})

    # Generate spectrum:    
    waveunit = sload['conditions']['waveunit']

    # Only `quantities` and `conditions` is required. The rest is just extra
    # details
    kwargs = {}
    
    # ... load slit if exists
    if 'slit' in sload:
        slit = {k:np.array(v) for k,v in sload['slit'].items()}
    else:
        slit = {}
        
    # ... load lines if exist
    if 'lines' in sload:
        dtypes = sload.get('_dtypes_lines', True)   # default to True
        if dtypes != True:
            dtypes = pd.read_json(dtypes)
        df = pd.read_json(sload['lines'], dtype=dtypes)
        df.sort_index(inplace=True)
        kwargs['lines'] = df
    else:
        kwargs['lines'] = None
        
    # ... load populations if exist
    if 'populations' in sload:
        pops = {}
        for molecule, isotopes in sload['populations'].items():
            pops[molecule] = {}
            for isotope, states in isotopes.items():
                isotope = int(isotope)    # cast to int
                pops[molecule][isotope] = {}
                for state, content in states.items():
                    pops[molecule][isotope][state] = {}
                    for k, v in content.items():
                        if k in ['vib', 'rovib']:  # pandas dataframes
                            dtypes = content.get('_dtypes_'+k, True)  # default True
                            if dtypes != True:
                                dtypes = pd.read_json(dtypes)
                            df = pd.read_json(v, dtype=dtypes)
                            df.sort_index(inplace=True)
                            pops[molecule][isotope][state][k] = df
                        elif k in ['_dtypes_vib', '_dtypes_rovib']:
                            pass
                        else:
                            pops[molecule][isotope][state][k] = v                        
        kwargs['populations'] = pops
    else:
        kwargs['populations'] = None
        
    # ... load other properties if exist
    for attr in ['units', 'cond_units', 'name']:
        try:
            kwargs[attr] = sload[attr]
        except KeyError:
            kwargs[attr] = None

    s = Spectrum(quantities=quantities,
                    conditions=conditions,
                    waveunit=waveunit,
                    **kwargs)
    
    # ... add slit 
    s._slit = slit
    
    return s 

def _fix_format(file, sload):
    ''' Test format / correct deprecated format:
    The goal is to still be able to load old format precomputed spectra, and
    fix their attribute names. Save them again to fix the warnigns definitly.
    '''
    
    # Fix deprecration syntax
    # ----------------
    try:
        sload['conditions']['waveunit']
    except KeyError as err:
        # deprecation: waveunit was named wavespace
        if 'wavespace' in sload['conditions']:
            sload['conditions']['waveunit'] = sload['conditions']['wavespace']
            del sload['conditions']['wavespace']
        else:
            raise KeyError("Spectrum 'conditions' dict should at least have a "+\
                           "'waveunit' key. Got: {0}".format(sload['conditions'].keys()))
                
    if 'isotope_identifier' in sload['conditions']:
        warn("File {0}".format(basename(file))+" has a deprecrated structure (key "+\
              "isotope_identifier replaced with isotope). Fixed, but regenerate "+\
            "database ASAP.", DeprecationWarning)
        sload['conditions']['isotope'] = sload['conditions'].pop('isotope_identifier')
        
    if 'air_pressure_mbar' in sload['conditions']:
        warn("File {0}".format(basename(file))+" has a deprecrated structure (key "+\
              "air_pressure_mbar replaced with pressure_mbar). Fixed, but regenerate "+\
            "database ASAP.", DeprecationWarning)
        sload['conditions']['pressure_mbar'] = sload['conditions'].pop('air_pressure_mbar')
        
    if 'isotope' in sload['conditions']:
        isotope = sload['conditions']['isotope']
        if not isinstance(isotope, string_types):
            warn("File {0}".format(basename(file))+" has a deprecrated structure (key "+\
                  "isotope is now a string). Fixed, but regenerate "+\
                "database ASAP.", DeprecationWarning)
            # Fix it:
            sload['conditions']['isotope'] = ','.join([str(k) for k in 
                 list_if_float(isotope)])
    
    if 'dbpath' in sload['conditions']:
        dbpath = sload['conditions']['dbpath']
        if not isinstance(dbpath, string_types):
            warn("File {0}".format(basename(file))+" has a deprecrated structure (key "+\
                  "dbpath is now a string). Fixed, but regenerate "+\
                "database ASAP.", DeprecationWarning)
            # Fix it:
            sload['conditions']['dbpath'] = ','.join([str(k).replace('\\','/') for k in 
                 list_if_float(dbpath)])  # list_if_float or just list??
    
    if 'selfabsorption' in sload['conditions']:
        self_absorption = sload['conditions']['selfabsorption']
        sload['conditions']['self_absorption'] = self_absorption
        del sload['conditions']['selfabsorption']
        
    # Fix all path names (if / are stored it screws up the JSON loading)
    # -----------------
    def fix_path(key):
        if key in sload['conditions']:
            path = sload['conditions'][key]
            if not isinstance(path, string_types):
                warn("File {0}".format(basename(file))+" has a deprecrated structure (key "+\
                      "{0} is now a string). Fixed, but regenerate ".format(key)+\
                    "database ASAP.", DeprecationWarning)
                # Fix it:
                sload['conditions'][key] = path.replace('\\','/')
                
    for param in ['database', 'levelspath', 'parfuncpath', # RADIS quantities
                  'results_directory', 'jobName', # other quantities
                  ]:
        fix_path(param)
        
    
    return sload
    

def plot_spec(file, what='radiance', title=True):
    ''' Plot a .spec file. *

    Parameters
    ----------

    file: str
        .spec file to load

    '''

    s = load_spec(file)

    try:
        s.plot(what)
    except KeyError:
        try:
            print((sys.exc_info()[0], sys.exc_info()[1]))
            s.plot(what + '_noslit') # who knows maybe it will work :)
            print(('Printing {0} instead'.format(what + '_noslit')))
        except:
            print((sys.exc_info()[0], sys.exc_info()[1]))
            # Plot something
            s.plot(s.get_vars()[0])
            print(('Printing {0} instead'.format(s.get_vars()[0])))

    if title:
        plt.title(basename(file))
        plt.tight_layout()

    return

# %% Database class
# ... loads database and manipulate it

class SpecDatabase():
    
    def __init__(self, path='.', filt='.spec', add_info=None, add_date='%Y%m%d',
                 verbose=True):
        ''' A Spectrum Database class to manage them all

        It basically manages a list of Spectrum JSON files, adding a Pandas
        dataframe structure on top to serve as an efficient index to visualize
        the spectra input conditions, and slice through the Dataframe with
        easy queries
        
        Parameters
        ----------
        
        path: str
            a folder to initialize the database
            
        filt: str
            only consider files ending with filt
        

        Example
        -------

            >>> db = SpecDatabase(r"path/to/database")     # create or loads database

            >>> db.update()  # in case something changed
            >>> db.see(['Tvib', 'Trot'])   # nice print in console

            >>> s = db.get('Tvib==3000')[0]  # get a Spectrum back
            >>> db.add(s)  # update database (and raise error because duplicate!)

        Note that SpectrumFactory objects can be configured to automatically update
        a database. 
        
        The function to auto retrieve a Spectrum from database on calculation
        time is a method of DatabankLoader class
        
        Note
        ----
        
        Database interaction is based on Pandas query functions. As such, it 
        requires all conditions to be either float, string, or boolean. List 
        won't work!

        '''

        # Assert name looks like a directory
        name, ext = splitext(path)

        if ext != '':
            raise ValueError('Database should be a directory: {0}'.format(path))

        if not exists(path):
            # create it
            os.mkdir(path)
            if verbose: print(('Database {0} initialised in {1}'.format(basename(path),
                              dirname(path))))
        else:
            if verbose: print(('Loading database {0}'.format(basename(path))))

        self.name = basename(name)
        self.path = path
        self.df = None
        self.verbose = verbose

        # default
        self.add_info = add_info
        self.add_date = add_date

        self.update(force_reload=True, filt=filt)

    def conditions(self):
        ''' Show conditions in database '''

        cond = list(self.df.columns)

        if len(cond) > 0:    
            cond.remove('file')
            cond.remove('Spectrum')

        return cond

    def see(self, columns=None, *args):
        ''' Shows Spectrum database will whole conditions (index=None) or
        specific conditions

        Parameters
        ----------

        columns: str, list of str, or None
            shows the conditions value for all cases in database. If None, all
            conditions are shown. Default None
            e.g.
            >>> db.see(['Tvib', 'Trot'])

        Notes
        -----

        Makes the 'file' column the index, and also discard the 'Spectrum' column
        (that holds all the data) for readibility

        '''

        if len(self) == 0:
            raise ValueError('Database is empty')

        if type(columns)==str:
            columns = [columns]+[k for k in args]
            
        dg  = self.df.set_index('file')  # note that this is a copy already.
                                    # dont try to modify the output of "see"
        del dg['Spectrum']          # for visibility"

        if columns is None: 
            return dg
        
        for c in columns:
            if not c in self.df.columns:
                raise ValueError('`{0}` is not a column name. Use one of {1}'.format(c, 
                                 self.df.columns))
            
        return dg.reindex(columns=columns)

    def view(self, columns=None, *args):
        ''' alias to df.see() '''
        
        return self.see(columns = columns, *args)

    def update(self, force_reload=False, filt='.spec'):
        ''' Reloads database, updates internal index structure and print it
        in <database>.csv

        Parameters
        ----------

        force_reload: boolean
            if True, reloads files already in database

        filt: str
            only consider files ending with `filt`
            
        '''

        path = self.path

        if force_reload:
            # Reloads whole database  (necessary on database init to create self.df
            files = [join(path, f) for f in os.listdir(path) if f.endswith(filt)]
            self.df = self._load_files(files=files)
        else:
            dbfiles = list(self.df['file'])
            files = [join(path, f) for f in os.listdir(path) if f not in dbfiles
                     and f.endswith(filt)]
            for f in files:
                self.df = self.df.append(self._load_file(f), ignore_index=True)

        # Print index
        self.print_index()

    def print_index(self, file=None):
        if file is None:
            file = join(self.path, basename(self.path)+'.csv')

        if len(self) > 0:
            try:
                self.see().to_csv(file)
            except PermissionError:
                warn('Database index could not be updated: {0}'.format(sys.exc_info()[1]))
        else:
            try:
                os.remove(file)  # if database existed but files were deleted
            except PermissionError:
                warn('Database index could not be updated: {0}'.format(sys.exc_info()[1]))
            except FileNotFoundError:
                pass

    def find_duplicates(self, columns=None):
        ''' Find spectra with same conditions '''

        dg = self.see(columns=columns).duplicated()


        if columns is None:
            columns = 'all'

        if self.verbose: print(('{0} duplicate(s) found'.format(dg.sum())+\
                               ' based on columns: {0}'.format(columns)))
        return dg

    def add(self, spectrum, **kwargs):
        ''' Add Spectrum to database, whether it's a Spectrum object or a file
        that stores one. Check it's not in database already.

        Parameters
        ----------

        spectrum: path to .spec file, or Spectrum object
            if Spectrum object: stores it in database first (using Spectrum.store()),
            then adds the file
            if path to file: will first copy the file in database folder, then
            adds the file

        **kwargs: **dict
            extra parameters used in the case where spectrum is a file and a .spec object
            has to be created (useless if `spectrum` is a file already). kwargs
            are forwarded to Spectrum.store() class. See Spectrum.store() or
            database.save() for more information

        Other Parameters
        ----------------
        
        Spectrum.store() parameters given as kwargs arguments. 
            
        file: str
            explicitely give a filename to save
    
        compress: boolean
            if True, removes all quantities that can be regenerated with s.update(),
            e.g, transmittance if abscoeff and path length are given, radiance if
            emisscoeff and abscoeff are given in non-optically thin case, etc.
            Default False

        add_info: list
            append these parameters and their values if they are in conditions
            example::

                nameafter = ['Tvib', 'Trot']

        discard: list of str
            parameters to exclude. To save some memory for instance
            Default [`lines`, `populations`]: retrieved Spectrum will loose the 
            line_survey ability, and plot_populations() (but it saves a ton of memory!)

        if_exists_then: 'increment', 'replace', 'error'
            what to do if file already exists. If increment an incremental digit
            is added. If replace file is replaced (yeah). If error (or anything else)
            an error is raised. Default `increment`

        Examples
        --------
        
        Simply write::
            
            db.add(s, discard=['populations'])

        '''
        
        # Check inputs
        if 'path' in kwargs:
            raise ValueError('path is an invalid Parameter. The database path '+\
                             'is used')

        # First, store the spectrum on a file
        # ... input is a Spectrum. Store it in database and load it from there
        if is_spectrum(spectrum):
            # add defaults
            if not 'add_info' in kwargs:
                kwargs['add_info'] = self.add_info
            if not 'add_date' in kwargs:
                kwargs['add_date'] = self.add_date
            file = spectrum.store(self.path, **kwargs)
            # Note we could have added the Spectrum directly
            # (saves the load stage) but it also serves to
            # check the file we just stored is readable

        # ... input is a file name. Copy it in database and load it
        elif type(spectrum) is str:
            if not exists(spectrum):
                raise FileNotFoundError('File doesnt exist: {0}'.format(spectrum))

            fd, name = split(spectrum)

            # Assert a similar case name is not in database already
            if spectrum in list(self.df['file']):
                raise ValueError('File already in database: {0}. Database filenames should be unique'.format(
                        spectrum))

            if abspath(fd) != abspath(self.path):
                # Assert file doesnt exist in database already
                if name in os.listdir(self.path):
                    raise ValueError('File already in database folder: {0}'.format(name)+\
                                     '. Use db.update() if you added it there manually')
                # Ok. Copy it.
                file = join(self.path, name)
                copy2(spectrum, file)

            else:
                warn('You are manually adding a file that is in the database folder directly. Consider using db.update()')
                file = spectrum

        else:
            raise ValueError('Unvalid Spectrum type: {0}'.format(type(spectrum)))

        # Then, load the Spectrum again (so we're sure it works!) and add the
        # information to the database
        self.df = self.df.append(self._load_file(file), ignore_index=True)

        # Update index .csv
        self.print_index()

        return

    def _load_files(self, files):
        ''' Parse files and generate a database
        '''
        db = []
        for f in files:
            db.append(self._load_file(f))

        return pd.DataFrame(db)

    def _load_file(self, file):
        ''' return Spectrum attributes for insertion in database.
        '''

        s = load_spec(file)

        if self.verbose: print(('loaded {0}'.format(basename(file))))

        out = s.get_conditions().copy()
        
        # Add filename, and a link Spectrum itself
        out.update({'file':basename(file), 'Spectrum':s})

        return out


    def get(self, conditions='', **kwconditions):
        '''   Returns a list of spectra that match given conditions

        Parameters
        ----------

        database: list of Spectrum objects
            the database

        conditions: str
            a list of conditions
            >>> get('Tvib==3000 & Trot==1500')

        kwconditions: dict
            an unfolded dict of conditions
            >>> get(Tvib=3000, Trot=1500)
            
        Other Parameters
        ----------------
        
        inplace: boolean
            if True, return the actual object in the database. Else, return
            copies. Default False

        Examples
        --------

        >>> spec_list = db.get('Tvib==3000 & Trot==1300')
        
        or
        
        >>> spec_list = db.get(Tvib=3000, Trot=1300)

        '''
                
        # Test inputs
        for (k,_) in kwconditions.items():
            if not k in self.df.columns:
                raise ValueError('{0} not a correct condition name. Use one of: {1}'.format(k, 
                                 self.df.columns))
        if len(self.df) == 0:
            warn('Empty database')
            return []
        
        inplace = kwconditions.pop('inplace', False)         # type: bool, default False

        # Unique condition method
        if conditions != '' and kwconditions != {}:
            raise ValueError("Please choose one of the two input format (str or dict) exclusively")

        if conditions == '' and kwconditions == {}:
            return list(self.df['Spectrum'])

        if conditions != '':
            dg = self.df.query(conditions)
        else:
            query = []
            for (k, v) in kwconditions.items():
                if isinstance(v, string_types):
                    query.append("{0} == '{1}'".format(k, v))
                else:
                    query.append('{0} == {1}'.format(k,v))
            # There is a limitation in numpy: a max of 32 arguments is required. 
            # Below we write a workaround when the Spectrum has more than 32 conditions
            if len(query) < 32:
                query = ' & '.join(query)
                if __debug__: printdbg('Database query: {0}'.format(query))
                dg = self.df.query(query)
            else:
                # cut in <32-long parts
                N = len(query)//32+1
                querypart = ' & '.join(query[::N])
                dg = self.df.query(querypart)
                for i in range(1, N+1):
                    querypart = ' & '.join(query[i::N])
                    if __debug__: printdbg('Database query: {0}'.format(querypart))
                    dg = dg.query(querypart)
            
        out = list(dg['Spectrum'])
                    
        if not inplace:
            out = [s.copy() for s in out]
        
        return out

    def get_unique(self, conditions='', **kwconditions):
        ''' Returns a spectrum that match given conditions. Raises an error
        if the spectrum is not unique 
        
        Parameters
        ----------
        
        see .get() for more details '''
        
        out = self.get(conditions, **kwconditions)

        if len(out) == 0:
            raise ValueError('Spectrum not found')
        elif len(out) > 1:
            raise ValueError('Spectrum is not unique ({0} match found)'.format(
                    len(out)))
        else:
            return out[0]

    def get_closest(self, scale_if_possible=True, **kwconditions):
        '''   Returns the Spectra in the database that is the closest to the input conditions

        Note that for non-numeric values only equals should be given.
        To calculate the distance all numeric values are scaled by their
        mean value in the database
        
        Parameters
        ----------
        
        kwconditions: named arguments 
            i.e: Tgas=300, path_length=1.5
            
        scale_if_possible: boolean
            if True, spectrum is scaled for parameters that can be computed 
            directly from spectroscopic quantities (e.g: 'path_length', 'molar_fraction')
            Default True
            
        Extra Parameters
        ----------------
        
        verbose: boolean
            print messages. Default True
            
        inplace: boolean
            if True, returns the actual object in database. Else, return a copy
            Default False
            
        '''
        
        scalable_inputs = ['mole_fraction', 'path_length']

        # Test inputs
        if kwconditions == {}:
            raise ValueError('Please specify filtering conditions. e.g: Tgas=300')
        
        # Inputs:
        verbose = kwconditions.pop('verbose', True)         # type: bool
        inplace = kwconditions.pop('inplace', False)        # type: bool
        
        for (k,_) in kwconditions.items():
            if not k in self.df.columns:
                raise ValueError('{0} not a correct condition name. Use one of: {1}'.format(k, 
                                 self.df.columns))

        dg = self.df.reindex(columns=list(kwconditions))
        
        if scale_if_possible:
            # Remove scalable inputs from distance calculation variables (unless
            # they're the last variable, because then it may screw things up)
            for k in scalable_inputs:
                if len(dg.columns) == 1:
                    break
                try:
                    del dg[k]
                except KeyError:
                    pass
                
#        raise
        
        mean = dict(dg.mean())
        std = dict(dg.std())
        dg['_d'] = 0  # distance (squared, actually)
        for k, v in kwconditions.items():
            if not k in dg.columns:
                continue
#            # add distance to all conditions planes. We regularize the different
#            # dimensions by working on normalized quantities: 
#            #     a  ->   (a-mean)/std  € [0-1]
#            # Distance becomes:
#            #     d^2 ->  sum((a-target)/std)^2
#            # Problem when std == 0! That means this dimension is not discrimant
#            # anyway
#            if std[k] == 0:
#                # for this conditions all parameters have the same value. 
#                dg['_d'] += (dg[k]-v)**2
#            else:
#                dg['_d'] += (dg[k]-v)**2/(std[k])**2
            # Eventually I chose to scale database with mean only (there was
            # an obvious problem with standard deviation scaling in the case of 
            # a non important feature containing very close datapoints that would
            # result in inappropriately high weights)
            dg['_d'] += (dg[k]-v)**2/mean[k]**2

        # self.plot('Tvib', 'Trot', dg['_d'])  # for debugging
        
        # Get spectrum with minimum distance to target conditions
        sout = self.df.ix[dg['_d'].idxmin(), 'Spectrum']     # type: Spectrum
        
        if not inplace:
            sout = sout.copy()

        # Scale scalable conditions
        if scale_if_possible:
            if 'path_length' in kwconditions:
                sout.rescale_path_length(kwconditions['path_length'])
            if 'mole_fraction' in kwconditions:
                sout.rescale_mole_fraction(kwconditions['mole_fraction'])

        if verbose:
            print(('------- \t'+'\t'.join(['{0}'.format(k) for k in kwconditions.keys()])))
            print(('Look up \t'+'\t'.join(['{0:.3g}'.format(v) for v in kwconditions.values()])))
            print(('Got     \t'+'\t'.join(['{0:.3g}'.format(sout.conditions[k]) for k in kwconditions.keys()])))

        return sout

    def plot(self, cond_x, cond_y, z_value=None, nfig=None):
        ''' Plot database points available:

        Parameters
        ----------

        cond_x, cond_y: str
            columns (conditions) of database.

        z_value: array, or None
            if not None, colors the 2D map with z_value. z_value is ordered
            so that z_value[i] corresponds to row[i] in database.

        Examples
        --------
    
        >>> db.plot(Tvib, Trot)     # plot all points calculated
    
    
        >>> db.plot(Tvib, Trot, residual)     # where residual is calculated by a fitting
                                              # procedure...

        '''
        # %%

        x = self.df[cond_x]
        y = self.df[cond_y]

        # Default
        fig = plt.figure(num=nfig)
        ax = fig.gca()
        ax.plot(x, y, 'ok')
        ax.set_xlabel(cond_x)
        ax.set_ylabel(cond_y)
        title = basename(self.path)

        # Overlay color
        if z_value is not None:
            assert(len(z_value))==len(self.df)

            z = np.array(z_value)**0.5  # because the lower the better

#            norm = cm.colors.Normalize(vmax=z.max(), vmin=z.min())
#            cmap = cm.PRGn


            xarr = np.linspace(min(x),max(x))
            yarr = np.linspace(min(y),max(y))
            mx, my = np.meshgrid(xarr,yarr)
            zgrid = griddata((x,y),z,(mx,my),method='linear')
            levels=np.linspace(min(z), max(z), 20)
            cs0 = ax.contourf(mx,my,zgrid,  levels=levels,
                               #linewidths=1,linestyles='dashed',
                               extend='both')

            ix0, iy0 = np.where(zgrid == zgrid.min())
            plt.plot((xarr[ix0], xarr[ix0]), (yarr.min(), yarr.max()), color='white', lw=0.5)
            plt.plot((xarr.min(), xarr.max()), (yarr[iy0], yarr[iy0]), color='white', lw=0.5)
            # lbls = plt.clabel(cs0, inline=1, fontsize=16,fmt='%.0fK',colors='k',manual=False)     # show labels

                              # %%

        plt.title(title)
        plt.tight_layout()

    def __len__(self):
        return len(self.df)



def in_database(smatch, db='.', filt='.spec'):
    ''' old function '''
    match_cond = smatch.get_conditions()
    for f in [f for f in os.listdir(db) if f.endswith(filt)]:
        fname = join(db, f)
        s = load_spec(fname)
        if s.get_conditions() == match_cond:
            return True
    return False

# %% Test
if __name__ == '__main__':

    from neq.test.spec.test_database import _run_testcases
    print(('Testing database.py: ', _run_testcases()))