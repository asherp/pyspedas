
from .mms_read_feeps_sector_masks_csv import mms_read_feeps_sector_masks_csv
from pytplot import get_data, store_data
import numpy as np

def mms_feeps_remove_sun(sensor_eyes, trange, probe='1', datatype='electron', data_units='intensity', data_rate='srvy', level='l2', suffix=''):
    
    sector_times, spin_sectors = get_data('mms'+probe+'_epd_feeps_' + data_rate + '_' + level + '_' + datatype + '_spinsectnum'+suffix)
    mask_sectors = mms_read_feeps_sector_masks_csv(trange=trange)
    out_vars = []

    top_sensors = [str(eye) for eye in sensor_eyes['top']]
    bot_sensors = [str(eye) for eye in sensor_eyes['bottom']]

    for sensor in top_sensors:
        var_name = 'mms'+str(probe)+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_top_'+data_units+'_sensorid_'+sensor+'_clean'

        top_data_tuple = get_data(var_name)
        if top_data_tuple is None:
            print('skipping variable: ' + var_name)
            continue
        times, top_data, top_energies = top_data_tuple

        if mask_sectors.get('mms'+probe+'imaskt'+sensor) is not None:
            bad_sectors = mask_sectors['mms'+probe+'imaskt'+sensor]

            for bad_sector in bad_sectors:
                this_bad_sector = np.where(spin_sectors == bad_sector)[0]
                if len(this_bad_sector) is not 0:
                    top_data[this_bad_sector] = np.nan

        try:
            store_data(var_name+'_sun_removed'+suffix, data={'x': times, 'y': top_data, 'v': top_energies})
            out_vars.append(var_name+'_sun_removed'+suffix)
        except Warning:
            continue

    if level is not 'sitl':
        for sensor in bot_sensors:
            var_name = 'mms'+str(probe)+'_epd_feeps_'+data_rate+'_'+level+'_'+datatype+'_bottom_'+data_units+'_sensorid_'+sensor+'_clean'

            bot_data_tuple = get_data(var_name)
            if bot_data_tuple is None:
                print('skipping: ' + var_name)
                continue
            times, bot_data, bot_energies = bot_data_tuple

            if mask_sectors.get('mms'+probe+'imaskb'+sensor) is not None:
                bad_sectors = mask_sectors['mms'+probe+'imaskb'+sensor]

                for bad_sector in bad_sectors:
                    this_bad_sector = np.where(spin_sectors == bad_sector)[0]
                    if len(this_bad_sector) is not 0:
                        bot_data[this_bad_sector] = np.nan

            try:
                store_data(var_name+'_sun_removed'+suffix, data={'x': times, 'y': bot_data, 'v': bot_energies})
                out_vars.append(var_name+'_sun_removed'+suffix)
            except Warning:
                continue
