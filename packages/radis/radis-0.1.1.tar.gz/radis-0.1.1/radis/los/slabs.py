# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 19:10:01 2017

@author: erwan

Classes to deal with multi-slabs configurations: 
- MergeSlabs for several Spectrum
- SerialSlabs to add several spectra along the line-of-path

One Slab is just a Spectrum object 

Todo
------

- transport emisscoeff too 
- emisscoeff default unit 

"""

from __future__ import print_function, absolute_import, division, unicode_literals

from radis.spectrum.spectrum import Spectrum, is_spectrum, NON_CONVOLUTED_QUANTITIES
from radis.phys.convert import nm2cm
from radis.misc.basics import merge_lists
from radis.misc.utils import FileNotFoundError
from radis.misc.arrays import count_nans
from radis.misc.debug import printdbg
from warnings import warn
import numpy as np
from numpy import exp, arange, allclose, abs, diff

# %% Slabs / Multi-layers / Radiative Transfer Equation (RTE)
#----------------------------------------------------------------------

def intersect(a, b):
    ''' Returns intersection of two dictionaries on values'''
    c = {}
    for k in set(a.keys()) & set(b.keys()): # work in Python 2?
        c[k] = a[k] if (a[k] == b[k]) else 'N/A'
    return c

def SerialSlabs(*slabs, **kwargs):
    ''' Compute the result of several slabs 

    
    Parameters    
    ----------
    
    slabs: list of Spectra, each representing a slab
        slabs       [0]     [1]  ............... [n]     
                     :       :                    :         \====
        light        *   ->  *        ->          *    ->    )===  observer
                                                            /====
            
    resample_wavespace: 'never', 'intersect', 'full'
        what to do when spectra have different wavespaces. 
        - If 'never', raises an error
        - If 'intersect', uses the intersection of all ranges, and resample
        spectra on the most resolved wavespace. 
        - If 'full', uses the overlap of all ranges, resample spectra on the 
        most resolved wavespace, and fill missing data with 0 emission and 0
        absorption
        Default 'never'
            
    out_of_bounds: 'transparent', 'nan', 'error'
        what to do if resampling is out of bounds. 'transparent': fills with 
        transparent medium. 'nan': fills with nan. 'error': raises an error. 
        Default 'nan'
                       

    Returns
    -------
    
    Spectrum object representing total emission and total transmittance as 
    observed at the output (slab[n+1]). Conditions and units are transported too,
    unless there is a mismatch then conditions are dropped (and units mismatch
    raises an error because it doesnt make sense)
    
    Use
    -------
    
        >>> s1 = calc_spectrum(...)
        >>> s2 = calc_spectrum(...)
        >>> s3 = SerialSlabs(s1, s2)
        
    Todo
    -------
    
    rewrite with 'recompute' list like in MergeSlabs
    
    '''

    # Check inputs, get defaults
    resample_wavespace = kwargs.get('resample_wavespace', 'never')   # default 'never'
    out_of_bounds = kwargs.get('out_of_bounds', 'nan')               # default 'nan'
    
    if resample_wavespace not in ['never', 'intersect', 'full']:
        raise ValueError("resample_wavespace should be one of: {0}".format
                         (', '.join(['never', 'intersect', 'full'])))
        
    if len(slabs)==0:
        raise ValueError('Empty list of slabs')
    
    elif len(slabs)==1:
        if not is_spectrum(slabs[0]):
            raise TypeError('SerialSlabs takes an unfolded list of Spectrum as '+\
                                 'argument: *list (got {0})'.format(type(slabs[0])))
        return slabs[0]

    else:  
        # recursively calculate serial slabs
        slabs = list(slabs)
        
        # TODO: correct class but it crashes anyway. 
        #  "All inputs must be Spectrum objects (got: <class 'neq.spec.spectrum.Spectrum'>)"
        
#        # Check all items are Spectrum
        for s in slabs:
            _check_valid(s)
            
        sn = slabs.pop(-1)            # type: Spectrum
        s = SerialSlabs(*slabs, resample_wavespace=resample_wavespace,
                        out_of_bounds=out_of_bounds)
        
        quantities = {}
        
        # make sure we use the same wavespace type (even if sn is in 'nm' and s in 'cm-1')
        waveunit = s.get_waveunit()  
        w = s.get('radiance_noslit', wunit=waveunit)[0]
        wn = sn.get('radiance_noslit', wunit=waveunit)[0]
        
        # Make all our slabs copies with the same wavespace range
        # (note: wavespace range may be different for different quantities, but
        # equal for all slabs)
        s, sn = resample_slabs(waveunit, resample_wavespace, out_of_bounds, 
                               s, sn)
        
        w, I = s.get('radiance_noslit', wunit=waveunit)  
        wn, In = sn.get('radiance_noslit', wunit=waveunit)
        _, Tn = sn.get('transmittance_noslit', wunit=waveunit)
        
        units = intersect(s.units, sn.units)
        
        if 'radiance_noslit' in s._q and 'radiance_noslit' in sn._q:
            # case where we may use SerialSlabs just to compute the products of all transmittances
            # Check units:
            unit = s.units['radiance_noslit']
            unitn = sn.units['radiance_noslit']
            if (unit != unitn):
                # convert unit of (w,I) into (wn, In)
                I = s.get_radiance_noslit(unitn)  # will crash if not possible
#                I = conv2(I, unit, unitn)  # will crash if not possible
                units['radiance_noslit'] = unitn
            quantities['radiance_noslit']=(w, I * Tn + In)
            
        if 'transmittance_noslit' in s._q:  # note that we dont need the transmittance in the inner
                                         # slabs to calculate the total radiance
            _, T = s.get('transmittance_noslit', wunit=waveunit)
            # Check units:
            if (s.units['transmittance_noslit'] != sn.units['transmittance_noslit']):
                # actually transmittance should have no units always...
                raise ValueError('Transmittance units arent the same in SerialSlabs '+\
                                 'calculation: {0} & {1}'.format(
                        s.units['radiance_noslit'], sn.units['radiance_noslit'])) 
            quantities['transmittance_noslit']=(w, Tn * T)
        
        # Get conditions (if they're different, fill with 'N/A')
        conditions = intersect(s.conditions, sn.conditions)
        conditions['waveunit'] = waveunit
        
        cond_units = intersect(s.cond_units, sn.cond_units)
        
        # name
        name = _serial_slab_names(s,sn)
        
        return Spectrum(quantities=quantities, conditions = conditions, 
                        cond_units = cond_units, units = units,
                        name=name)

def _serial_slab_names(s, sn):
    name_s = s.get_name()
    name_sn = sn.get_name()
    if '//' in name_s and not '>>' in name_s:
        name_s = '({0})'.format(name_s)
    if '//' in name_sn:
        name_sn = '({0})'.format(name_sn)
    return '{0}>>{1}'.format(name_s, name_sn)

def _check_valid(s):
    ''' Check s is a valid Spectrum object. Raises an error if not '''
    
    if not is_spectrum(s):
        raise TypeError('All inputs must be Spectrum objects (got: {0})'.format(
                type(s)))
    sdict = s._get_items()
    for k in sdict.keys():
        if count_nans(sdict.get(k))>0:
            warn('Nans detected in Spectrum object for multi-slab operation. '+\
                 'Results may be wrong!')
    
    return True

def _has_quantity(quantity, *slabs):
    slabs = list(slabs)
    b = True
    for s in slabs:
        b *= quantity in slabs
    return b

def resample_slabs(waveunit, resample_wavespace, out_of_bounds='nan', *slabs):
    ''' Resample slabs on the same wavespace: if the range are differents, 
    depending on the mode we may fill with optically thin media, or raise an
    error 
    
    
    Parameters    
    ----------
    
    waveunit: 'nm', 'cm-1'
        which wavespace we're working in 
    
    resample_wavespace: 'never', 'intersect', 'full'
        what to do when spectra have different wavespaces. 
        - If 'never', raises an error
        - If 'intersect', uses the intersection of all ranges, and resample
        spectra on the most resolved wavespace. 
        - If 'full', uses the overlap of all ranges, resample spectra on the 
        most resolved wavespace, and fill missing data with 0 emission and 0
        absorption
        Default 'never'
        
    out_of_bounds: 'transparent', 'nan', 'error'
        what to do if resampling is out of bounds. 'transparent': fills with 
        transparent medium. 'nan': fills with nan. 'error': raises an error. 
        Default 'nan'
        
    *slabs: list of Spectrum objects
    

    Returns
    -------
    
    slabs: list of Spectrum objects
        resampled copies of inputs Spectra. All now have the same wavespace
        
    ''' 

    # Check wavespace is the same
    def same_wavespace(wl):
        if not all([len(w) == len(wl[0]) for w in wl[1:]]):
            return False
        elif not all([allclose(w, wl[0]) for w in wl[1:]]):
            return False
        else:
            return True
        
    # Work on copies
    slabs = [s.copy() for s in slabs]
    
    # Get all keys
    keys = merge_lists([s.get_vars() for s in slabs])
    
    for k in keys:
        # We ensure all quantities are resampled. Note that .resample() deals 
        # with all quantities so usually spectra are fully corrected after the 
        # first iteration. However, it also deals with cases where quantities 
        # have different wavespaces (ex: radiance and radiance_noslit are not
        # defined on the same range)
        slabsk = [s for s in slabs if k in s.get_vars()]  # note that these are
                                        # references to the actual Spectrum copy
        wl = [s.get(k, wunit=waveunit)[0] for s in slabsk]
        if not same_wavespace(wl):
            # resample slabs if allowed
            if resample_wavespace == 'never':
                raise ValueError('All wavelengths/wavenumbers must be the same for '+\
                                 'multi slabs configurations. Consider using `resample_wavespace` '+\
                                 '= `intersect` or `full`')
            elif resample_wavespace == 'full':
                # ... get bounds
                wmin = min([w.min() for w in wl])   # minimum of all 
                wmax = max([w.max() for w in wl])   # maximum of all 
                dw = min([abs(diff(w)).min() for w in wl])  # highest density
                wnew = arange(wmin, wmax+dw, dw)
                # ... copy the array of slabs not to modify the input
                # ... slabs themselves
                for s in slabsk:
                    s.resample(wnew, unit=waveunit, if_conflict_drop='convoluted',
                               out_of_bounds=out_of_bounds)
                # note: s.resample() fills with 0 when out of bounds
            elif resample_wavespace == 'intersect':
                # ... get bounds
                wmin = max([w.min() for w in wl])   # maximum of all 
                wmax = min([w.max() for w in wl])   # minimum of all 
                dw = min([abs(diff(w)).min() for w in wl])  # highest density
                wnew = arange(wmin, wmax+dw, dw)
                if len(wnew)==0:
                    raise ValueError('Intersect range is empty')
                # ... copy the array of slabs not to modify the input
                # ... slabs themselves
                for s in slabsk:
                    s.resample(wnew, unit=waveunit, if_conflict_drop='convoluted',
                               out_of_bounds=out_of_bounds)
                # note: s.resample() fills with 0 when out of bounds
        # Now all our slabs have the same wavespace
            
    return slabs
    
def MergeSlabs(*slabs, **kwargs):
    ''' Combines several slabs into one. Useful to calculate multi-gas slabs. 
    Linear absorption coefficient is calculated as the sum of all linear absorption
    coefficients, and the RTE is recalculated to get the total radiance

    
    Parameters    
    ----------
    
    slabs: list of Spectra, each representing a slab
        If given in conditions, all path_length have to be same

    kwargs input
    --------

    resample_wavespace: 'never', 'intersect', 'full'
        what to do when spectra have different wavespaces. 
        - If 'never', raises an error
        - If 'intersect', uses the intersection of all ranges, and resample
        spectra on the most resolved wavespace. 
        - If 'full', uses the overlap of all ranges, resample spectra on the 
        most resolved wavespace, and fill missing data with 0 emission and 0
        absorption
        Default 'never'
        
    out_of_bounds: 'transparent', 'nan', 'error'
        what to do if resampling is out of bounds. 'transparent': fills with 
        transparent medium. 'nan': fills with nan. 'error': raises an error. 
        Default 'nan'

    optically_thin: boolean
        if True, merge slabs in optically thin mode. Default False 
                            
    verbose: boolean
        if True, print messages and warnings. Default True
        

    Returns
    -------
    
    Spectrum object representing total emission and total transmittance as 
    observed at the output. Conditions and units are transported too,
    unless there is a mismatch then conditions are dropped (and units mismatch
    raises an error because it doesnt make sense)
    
    
    Examples
    -------
    
    Merge two spectra calculated with different species (true only if broadening
    coefficient dont change much):
    
        >>> from radis import calc_spectrum, MergeSlabs
        >>> s1 = calc_spectrum(...)
        >>> s2 = calc_spectrum(...)
        >>> s3 = MergeSlabs(s1, s2)
        
    Load a spectrum precalculated on several partial spectral ranges, for a same 
    molecule (i.e, partial spectra are optically thin on the rest of the spectral 
    range)
    
        >>> from radis import load_spec, MergeSlabs
        >>> spectra = []
        >>> for f in ['spec1.spec', 'spec2.spec', ...]:
        >>>     spectra.append(load_spec(f))
        >>> s = MergeSlabs(*spectra, resample_wavespace='full', out_of_bounds='transparent')
        >>> s.update()   # Generate missing spectral quantities
        >>> s.plot()
        
    '''
    
    # inputs (Python 2 compatible)
    resample_wavespace = kwargs.get('resample_wavespace', 'never')   # default 'never'
    out_of_bounds = kwargs.get('out_of_bounds', 'nan')               # default 'nan'
    optically_thin = kwargs.pop('optically_thin', False)             # default False
    
    verbose = kwargs.pop('verbose', True)             # type: bool
    debug = kwargs.pop('debug', False)                # type: bool
    
    # Check inputs
    if resample_wavespace not in ['never', 'intersect', 'full']:
        raise ValueError("resample_wavespace should be one of: {0}".format
                         (', '.join(['never', 'intersect', 'full'])))
        
    if len(slabs)==0:
        raise ValueError('Empty list of slabs')
    
    elif len(slabs)==1:
        if not is_spectrum(slabs[0]):
            raise TypeError('MergeSlabs takes an unfolded list of Spectrum as '+\
                                 'argument: (got {0})'.format(type(slabs[0])))
        return slabs[0]

    else:  # calculate serial slabs
        
        slabs = list(slabs)
        
#        # Check all items are valid Spectrum objects
        for s in slabs:
            _check_valid(s)
        
        # Just check all path_lengths are the same if they exist
        try:
            path_lengths = [s.conditions['path_length'] for s in slabs]
        except KeyError:
            raise KeyError('path_length must be defined for all MergeSlabs inputs')
        if not all([L == path_lengths[0] for L in path_lengths[1:]]):
            raise ValueError('path_length must be equal for all MergeSlabs inputs'+\
                             '  (got {0})'.format(path_lengths))
        
        # make sure we use the same wavespace type (even if sn is in 'nm' and s in 'cm-1')
        waveunit = slabs[0].get_waveunit()  
        # Make all our slabs copies with the same wavespace range
        # (note: wavespace range may be different for different quantities, but
        # equal for all slabs)
        slabs = resample_slabs(waveunit, resample_wavespace, out_of_bounds, *slabs)
        w_noconv = slabs[0]._get_wavespace()
    
        # %%
        for s in slabs:
            if not 'abscoeff' in list(s._q.keys()):
                try:
                    s.get('absorbance', wunit=waveunit)
                    s.conditions['path_length']
#                    s['abscoeff'] = (w, A/s.conditions['path_length'])
                except KeyError:
                    raise KeyError('If abscoeff is not a calculated spectrum quantity '+\
                                   'then both `absorbance` and conditions[`path_length`] '+\
                                   'should be given for MergeSlabs inputs')
        
        
        # Get conditions
        conditions = slabs[0].conditions
        conditions['waveunit'] = waveunit
        cond_units = slabs[0].cond_units
        units = slabs[0].units
        for s in slabs[1:]:
            conditions = intersect(conditions, s.conditions)
            cond_units = intersect(cond_units, s.cond_units)
            units = intersect(units, s.units)
        
        # %% Get quantities that should be calculated 
            
        requested = merge_lists([s.get_vars() for s in slabs])
        recompute = requested.copy()
        if ('radiance_noslit' in requested and not optically_thin):
            recompute.append('emisscoeff')
            recompute.append('abscoeff')
        if 'abscoeff' in recompute and 'path_length' in conditions:
            recompute.append('absorbance')
            recompute.append('transmittance_noslit')
                    
        path_length = conditions['path_length']

        # %% Calculate new quantites
        added = {}        
        
        # ... absorption coefficient (cm-1)
        if 'abscoeff' in recompute:
            #TODO: deal with all cases
            if __debug__: printdbg('... merge: calculating abscoeff k=sum(k_i)')
            abscoeff_eq = np.sum([s.get('abscoeff', wunit=waveunit)[1] for s in slabs], axis=0)
            assert len(w_noconv) == len(abscoeff_eq)
            added['abscoeff'] = (w_noconv, abscoeff_eq)
        
        if 'absorbance' in recompute:
            if 'abscoeff' in added:
                if __debug__: printdbg('... merge: calculating absorbance A=k*L')
                _, abscoeff_eq = added['abscoeff']            
                absorbance_eq = abscoeff_eq*path_length
            else:
                raise NotImplementedError('recalculate abscoeff first')
            added['absorbance'] = (w_noconv, absorbance_eq)
        
        # ... transmittance
        if 'transmittance_noslit' in recompute:    
            if 'absorbance' in added:
                if __debug__: printdbg('... merge: calculating transmittance T=exp(-A)')
                _, absorbance_eq = added['absorbance']
                transmittance_noslit_eq = exp(-absorbance_eq)
            else:
                raise NotImplementedError('recalculate absorbance first')
            added['transmittance_noslit'] = (w_noconv, transmittance_noslit_eq)

        # ... emission coefficient
        if 'emisscoeff' in recompute:
            emisscoeff_eq = np.zeros_like(w_noconv)
            for i, s in enumerate(slabs):
                # Manual loop in case all Slabs dont have the same keys
                # Could also do a slab.update() first then sum emisscoeff directly
                if 'emisscoeff' in list(s._q.keys()):
                    if __debug__: printdbg('... merge: calculating emisscoeff: j+=j_i')
                    _, emisscoeff = s.get('emisscoeff', wunit=waveunit)
                elif optically_thin and 'radiance_noslit' in list(s._q.keys()):
                    if __debug__: printdbg('... merge: calculating emisscoeff: j+=I_i/L '+\
                                    '(optically thin case)')
                    _, I = s.get('radiance_noslit', wunit=waveunit)
                    emisscoeff = I/path_length
                    emisscoeff_eq += emisscoeff
                else:
                    wI, I = s.get('radiance_noslit', wunit=waveunit)
                    if __debug__: printdbg('... merge: calculating emisscoeff j+=[k*I/(1-T)]_i)')
                    try:
                        wT, T = s.get('transmittance_noslit', wunit=waveunit)
                        wk, k = s.get('abscoeff', wunit=waveunit)
                    except KeyError:
                        raise KeyError('Need transmittance_noslit and abscoeff to '+\
                                       'recompute emission coefficient')
                    b = (T == 1)  # optically thin mask
                    emisscoeff = np.zeros_like(T)
                    emisscoeff[b] = I[b]/path_length     # optically thin case
                    emisscoeff[~b] = I[~b]/(1-T[~b])*k[~b]
                emisscoeff_eq += emisscoeff
            added['emisscoeff'] = (w_noconv, emisscoeff_eq)
            
        # ... derive global radiance (result of analytical RTE solving)
        if 'radiance_noslit' in recompute:
            if 'emisscoeff' in added and optically_thin:
                if __debug__: printdbg('... merge: recalculating radiance_noslit I=j*L(optically_thin)')
                (_, emisscoeff_eq) = added['emisscoeff']
                radiance_noslit_eq = emisscoeff_eq * path_length  # optically thin 
            elif ('emisscoeff' in added and 'transmittance_noslit' in added and
                'abscoeff' in added):
                if __debug__: printdbg('... merge: recalculating radiance_noslit I=j/k*(1-T)')
                (_, emisscoeff_eq) = added['emisscoeff']
                (_, abscoeff_eq) = added['abscoeff']
                (_, transmittance_noslit_eq) = added['transmittance_noslit']
                b = (abscoeff_eq == 0) # optically thin mask
                radiance_noslit_eq = np.zeros_like(emisscoeff_eq)
                radiance_noslit_eq[b] = emisscoeff_eq[b] * path_length  # optically thin limit
                radiance_noslit_eq[~b] = emisscoeff_eq[~b]/abscoeff_eq[~b]*(1-
                                  transmittance_noslit_eq[~b])
            elif optically_thin:
                if __debug__: printdbg('... merge: recalculating radiance_noslit I=sum(I_i) (optically thin)')
                radiance_noslit_eq = np.zeros_like(w_noconv)
                for s in slabs:
                    if 'radiance_noslit' in list(s._q.keys()):
                        radiance_noslit_eq += s.get('radiance_noslit', wunit=waveunit)[1]
                    else:
                        raise KeyError('Need radiance_noslit for all slabs to '+\
                                       'recalculate for the MergeSlab (could also '+\
                                       'get it from emisscoeff but not implemented)')
            else:
                if optically_thin:
                    raise ValueError('Missing data to recalculate radiance_noslit'+\
                                     '. Try optically_thin mode?')
                else:
                    raise ValueError('Missing data to recalculate radiance_noslit')
            added['radiance_noslit'] = (w_noconv, radiance_noslit_eq)
        
        # ... emissivity no slit
        if 'emissivity_noslit' in requested:
            added['emissivity_noslit'] = w_noconv, np.ones_like(w_noconv)*np.nan
#            if verbose: 
#                warn('emissivity dropped during MergeSlabs') 
            # Todo: deal with equilibrium cases?
        
        # Store output
        quantities = {}
        for k in requested:
            quantities[k] = added[k]
            
        # name
        name = '//'.join([s.get_name() for s in slabs])
        
        # TODO: check units are consistent in all slabs inputs
        return Spectrum(quantities=quantities, conditions = conditions, 
                        cond_units = cond_units, units = units,
                        name=name)

# %% Tests
        
def _test_merge_slabs(verbose=True, plot=True, warnings=True, debug=False, 
                      *args, **kwargs):
    ''' Merge 10 slabs with 1/10 of concentration, and compare the results. 
    Ensure error is < 0.1%
    
    Note that we won't have exactly the same results as the broadening is not
    updated in MergeSlabs 
    '''
    
    from neq.spec import load_spec
    import matplotlib.pyplot as plt
    from neq.test.utils import getTestFile
    
    b = True
    
    for optically_thin in [True, False]:
    
        s1 = load_spec(getTestFile('CO_Tgas1500K_mole_fraction0.01.spec'))
        s2 = load_spec(getTestFile('CO_Tgas1500K_mole_fraction0.5.spec'))
        s1.update(optically_thin=optically_thin)
        s2.update(optically_thin=optically_thin)
    #    s1 = sf.non_eq_spectrum(Tgas, Tgas, mole_fraction=0.01)
    #    s2 = sf.eq_spectrum(Tgas, mole_fraction=N*0.01)
    #    slist = [s1.copy()]*N
        slist = [s1]*50
        s1N = MergeSlabs(*slist, optically_thin=optically_thin, debug=debug)
        
    #    print(s2.compare_with(s1N, only_spectra=True))
    #    print(np.allclose(s2.get('radiance_noslit'), s1N.get('radiance_noslit')))
    #    print('Max error: {0:.2f}%'.format(np.abs(s2.get('radiance_noslit')[1]/
    #          s1N.get('radiance_noslit')[1]-1).max()*100))
        
        b1 = np.isclose(s2.get_power(), s1N.get_power(), 1.5e-2)
        if verbose:
            print('Compare 50x[CO=0.01] vs 1x[CON=0.5] (optically thin: {1}): {0}'.format(
                    b1, optically_thin))
            print('... Difference: {0:.2f}%'.format(abs(s1N.get_power()/s2.get_power()-1)*100))
        b *= b1
    
        if plot:
            for k in ['radiance_noslit']: #, 'transmittance_noslit']:
                s2.plot(k, lw=3,label='1x[CO=0.5]')
                s1N.plot(k, nfig='same', label='50x[CO=0.01]')
                plt.legend()
                plt.title('Optically thin: {0}'.format(optically_thin))
                plt.tight_layout()
            
    return bool(b)
#        
        
def _test(verbose=True, plot=True, debug=False, warnings=True, *args, **kwargs):
    
    b = True
    
    b *= _test_merge_slabs(verbose=verbose, plot=plot, debug=debug, warnings=warnings,
                           *args, **kwargs)
    
    # Todo: add a test with _serial_slabs ... For instance the Sebastien Depraz reference case
        
    return bool(b)


if __name__ == '__main__':
    print('Testing merge slabs: ', _test(verbose=True))
