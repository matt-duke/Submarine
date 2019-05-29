import logging
logger = logging.getLogger()

import os
from os.path import join

class Paths(dict):
    def __init__(self):
        dict.__init__(self)
        
    def get(self, key):
        if key not in self.keys():
            logger.error('{} not in common.Paths'.format(key))
        else:
            return self[key]