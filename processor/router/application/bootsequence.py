#!/usr/bin/python3

import platform
import logging
import sys
import os
from os.path import join
from time import sleep

## Initial setup
try:
    import common
    import core
except:
    sys.path.append(os.path.abspath(join(os.getcwd(),'../..','common')))
    import common
    import core

def add_paths():
    root = os.getcwd()
    if common.platform == 'Linux':
        volatile = '/tmp'
        config = '/configuration'
        database = '/db'
        base = '/'
        
    else:
        volatile = root
        config = os.path.abspath(join(os.getcwd(),'../..','configuration'))
        database = root
        base = root
   
    common.Paths['DEBUG_LOG'] = join(volatile,'debug.log')
    common.Paths.critical('CONFIG',join(config, 'config.ini'))
    common.Paths.critical('CONFIG_SCHEMA',join(db, 'schema.ini'))
    common.Paths.critical('VERSION',join(config, 'expected_sw_config.json'))
    common.Paths.critical('UBOOT',join(base, 'uboot'))
    common.Paths.critical('VOLATILE',volatile)

if __name__ == '__main__': 
    common.CvtManager = common.CvtManager()
    common.CVT = common.CvtManager.cvt