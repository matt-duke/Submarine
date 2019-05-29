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
        
    else:
        volatile = root
        config = os.path.abspath(join(os.getcwd(),'../..','configuration'))
        common.Paths['DATABASE'] = join(root,'data.db')
   
    common.Paths.critical('DEBUG_LOG', join(volatile,'debug.log'))
    common.Paths.critical('CONFIG',join(config, 'config.ini'))
    common.Paths.critical('CONFIG_SCHEMA',join(config, 'schema.ini'))
    common.Paths.critical('VERSION',join(config, 'version.json'))
    common.Paths.critical('VOLATILE',volatile)
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger=logging.getLogger('bootsequence')
        
    common.CDS = common.CommonDataStructure()
    common.CDS.write('platform', platform.system())
    common.platform = platform.system()
    common.CDS.write('testmode', {'Linux':False, 'Windows':True}[common.CDS.read('platform')])
    common.testmode = common.CDS.read('testmode')
    
    common.Paths = common.Paths()
    add_paths()
    
    common.OpMode = StateMachines.OpModeMachine()
    common.Active = StateMachines.ActiveMachine()
    
    while not common.OpMode.is_normal() and not common.OpMode.is_critical():
        curr_state = common.OpMode.state
        print('loop')
        try:
            logger.info('requesting transition')
            tmp = common.OpMode.next()
        except MachineError as e:
            logger.error(e)
        
        while common.OpMode.state == curr_state:
            pass
        