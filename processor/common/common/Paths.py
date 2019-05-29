import logging
logger = logging.getLogger(__name__)

import os
from os.path import join

class Paths(dict):
    def __init__(self):
        dict.__init__(self)
    
    def __setitem__(self, key, val):
        self.add(key, val, False)
        
    def critical(self, key, val):
        self.add(key, val, True)
    
    def add(self, key, val, critical=False):
        val = (val, critical)
        dict.__setitem__(self, key, val)

    def __getitem__(self, key):
        try:
            return dict.get(self, key)[0]
        except KeyError:
            logger.error('{} not in common.Paths'.format(key))

    def get(self, key):
        try:
            return dict.get(self, key)[0], dict.get(self, key)[1]
        except KeyError:
            logger.error('{} not in common.Paths'.format(key))
	