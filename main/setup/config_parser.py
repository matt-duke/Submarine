import configparser
import os
from pathlib import Path
import common
import logging
logger = logging.getLogger(__name__)

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
            common.sensors[option] = common.Sensor(option, int(data[0]), bool(data[1]))
        else:
            logger.warning('Unknown option: SENSOR:{}'.format(option))
    
    return config