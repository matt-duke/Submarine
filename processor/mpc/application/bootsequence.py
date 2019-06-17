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

import StateMachines
from transitions.core import MachineError

    
def add_paths():
    root = os.getcwd()
    if common.platform == 'Linux':
        volatile = '/tmp'
        config = '/configuration'
        common.Paths['DATABASE'] = '/media/data.db'
        base = '/'
        
    else:
        volatile = root
        config = os.path.abspath(join(os.getcwd(),'../..','configuration'))
        common.Paths['DATABASE'] = join(root,'data.db')
        base = root
   
    common.Paths['DEBUG_LOG'] = join(volatile,'debug.log')
    common.Paths.critical('CONFIG',join(config, 'config.ini'))
    common.Paths.critical('CONFIG_SCHEMA',join(config, 'schema.ini'))
    common.Paths.critical('VERSION',join(config, 'expected_sw_config.json'))
    common.Paths.critical('UBOOT',join(base, 'uboot'))
    common.Paths.critical('VOLATILE',volatile)
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger=logging.getLogger('bootsequence')
        
    common.CvtManager = common.CvtManager()
    common.CVT = common.CvtManager.cvt
    common.CVT.platform = platform.system()
    common.platform = platform.system()
    common.CVT.testmode = {'Linux':False, 'Windows':True}[common.CVT.platform]
    common.testmode = common.CVT.testmode
    
    common.Paths = common.Paths()
    add_paths()
    
    #common.ModuleServer = common.ModuleServer()
    
    common.OpMode = StateMachines.OpModeMachine()
    common.Active = StateMachines.ActiveMachine()
    
    while not common.OpMode.is_normal() and not common.OpMode.is_critical():
        try:
            logger.info('requesting transition')
            common.OpMode.next()
        except MachineError as e:
            logger.error(e)
        common.OpMode.ready.wait()
        
    while True:
        pass
        