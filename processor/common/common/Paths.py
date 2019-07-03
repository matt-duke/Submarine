import logging
logger = logging.getLogger(__name__)

import os
from os.path import join


folders = {
    "ROOT": "/image",
    "VOLATILE": "/tmp",
    "DATABASE": "/image/db",
    "CONFIGURATION": "/persistent"
}

paths = {
    "DEBUG_LOG":join(folders["VOLATILE"],"debug.log"),
    "CONFIG": join(folders["CONFIGURATION"], "config.ini"),
    "DEFAULT_CONFIG": join(folders["DATABASE"], "config.ini")
    "CONFIG_SCHEMA": join(folders["DATABASE"], "schema.ini")
    "VERSION": join(folders["CONFIGURATION"], "expected_sw_config.json"),
    "UBOOT": join("/", "uboot.sh"
}

class Paths(dict):
    def __init__(self):
        dict.__init__(self)
        
        default = common.defaults.get()
        for key, path in default['paths'].items():
            p = os.path.join(default[path['basename']], path['filename'])
            common.Paths.add(key, p)
            
        for key, path in self.items():
            if not os.path.exists(path):
                self.logger.info('Generating empty file for {}'.format(path))
                open(path, 'w').close()
    
    def __add(self, key, val, critical=True):
        val = (val, critical)
        dict.__setitem__(self, key, val)

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key):
        try:
            return dict.get(self, key)[0], dict.get(self, key)[1]
        except KeyError:
            logger.error('{} not in common.Paths'.format(key))
	