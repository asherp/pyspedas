import numpy as np 
from pytplot import get_data, store_data
from pyspedas import tnames

def mms_fgm_remove_flags(probe, data_rate, level, instrument, suffix=''):
    """
    This function removes data flagged by the FGM 'flag' variable (flags > 0), 
    in order to only show science quality data by default.
    
    Parameters:
        probe : str or list of str
            probe or list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for FGM include 'brst' 'fast' 'slow' 'srvy'. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

    """
    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(level, list): level = [level]

    tplot_vars = set(tnames())

    for this_probe in probe:
        for this_dr in data_rate:
            for this_lvl in level:
                flag_var = 'mms'+str(this_probe)+'_'+instrument+'_flag_'+this_dr+'_'+this_lvl+suffix
                times, flags = get_data('mms'+str(this_probe)+'_'+instrument+'_flag_'+this_dr+'_'+this_lvl+suffix)
                flagged_data = np.where(flags != 0.0)[0]

                for var_specifier in ['_b_gse_', '_b_gsm_', '_b_dmpa_', '_b_bcs_']:
                    var_name = 'mms'+str(this_probe)+'_'+instrument+var_specifier+this_dr+'_'+this_lvl+suffix
                    if var_name in tplot_vars:
                        times, var_data = get_data(var_name)
                        var_data[flagged_data] = np.nan
                        store_data(var_name, data={'x': times, 'y': var_data})
