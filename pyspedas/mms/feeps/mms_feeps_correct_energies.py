'''
 PURPOSE:
       This function modifies the energy table in FEEPS spectra (intensity, count_rate, counts) variables
       using the function: mms_feeps_energy_table (which is s/c, sensor head and sensor ID dependent)

 NOTES:
     BAD EYES are replaced by NaNs

'''

import pytplot
from pytplot import get_data, store_data
from .mms_feeps_energy_table import mms_feeps_energy_table
from pyspedas import tnames

def mms_feeps_correct_energies(probes, data_rate, level='l2', suffix=''):

    types = ['top', 'bottom']
    sensors = range(1, 13)
    units_types = ['intensity', 'count_rate']

    for probe in probes:
        for sensor_type in types:
            for sensor in sensors:
                if sensor >= 6 and sensor <= 8: 
                    species = 'ion'
                else: 
                    species = 'electron'

                for units in units_types:
                    var_name = tnames('mms'+probe+'_epd_feeps_'+data_rate+'_'+level+'_'+species+'_'+sensor_type+'_'+units+'_sensorid_'+str(sensor))

                    if var_name == []:
                        continue
                    else:
                        var_name = var_name[0]

                    var_data = get_data(var_name+suffix)
                    if var_data is not None:
                        times, data = var_data
                    else:
                        continue

                    energies = pytplot.data_quants[var_name+suffix].spec_bins.values
                    energy_map = mms_feeps_energy_table(probe, sensor_type[0:3], sensor)

                    try:
                        store_data(var_name+suffix, data={'x': times, 'y': data, 'v': energy_map})
                    except:
                        continue