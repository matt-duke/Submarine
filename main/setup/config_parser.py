import configparser
import os
from pathlib import Path
import common

def config_parser(path):
    path = Path(path)
    config = configparser.ConfigParser()
    config._interpolation = configparser.ExtendedInterpolation()
    config.read(path)
    for option in config.options('PATHS'):
        data = Path(config.get('PATHS', option))
        if not os.path.isdir(data):
            os.mkdir(data)

    for option in config.options('SENSOR'):
        data = config.get('SENSOR', option)
        if option == 'validitytimeout':
            common.Sensor.validity_timeout = int(data)
            continue
        data = data.split(',')
        if len(data) == 2:
            common.sensors[option] = common.Sensor()
            common.sensors[option].id = int(data[0])
            common.sensors[option].type = int(data[1])
        else:
            print('Unknown option: SENSOR:{}'.format(option))
    
    return config