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
    
    return config
