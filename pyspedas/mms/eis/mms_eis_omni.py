import numpy as np
from pytplot import get_data, store_data, options
from ...utilities.tnames import tnames

def mms_eis_omni(probe, species='proton', datatype='extof', suffix='', data_units='flux', data_rate='srvy'):
    """
    This function will calculate the omni-directional EIS spectrograms, and is automatically called from mms_load_eis
    
    Parameters:
        probe: str
            probe #, e.g., '4' for MMS4
        data_units: str
            'flux' 
        datatype: str
            'extof' or 'phxtof'
        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst'
        suffix: str
            suffix of the loaded data

    Returns:
        Name of tplot variable created.
    """
    
    probe = str(probe)
    species_str = datatype + '_' + species
    if data_rate == 'brst':
        prefix = 'mms' + probe + '_epd_eis_brst_'
    else: 
        prefix = 'mms' + probe + '_epd_eis_'

    telescopes = tnames(pattern=prefix + species_str + '_*' + data_units + '_t?'+suffix)

    if len(telescopes) == 6:
        time, data, energies = get_data(telescopes[0])
        flux_omni = np.zeros((len(time), len(energies)))
        for t in telescopes:
            time, data, energies = get_data(t)
            flux_omni = flux_omni + data

        store_data(prefix + species_str + '_' + data_units + '_omni' + suffix, data={'x': time, 'y': flux_omni/6., 'v': energies})
        options(prefix + species_str + '_' + data_units + '_omni' + suffix, 'spec', 1)
        options(prefix + species_str + '_' + data_units + '_omni' + suffix, 'ylog', 1)
        options(prefix + species_str + '_' + data_units + '_omni' + suffix, 'zlog', 1)
        options(prefix + species_str + '_' + data_units + '_omni' + suffix, 'yrange', [14, 45])
        options(prefix + species_str + '_' + data_units + '_omni' + suffix, 'Colormap', 'jet')
        return prefix + species_str + '_' + data_units + '_omni' + suffix
    else:
        print('Error, problem finding the telescopes to calculate omni-directional spectrograms')
        return None
