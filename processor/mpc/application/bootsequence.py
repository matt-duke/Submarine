#!/bin/python3

import platform
import logging
import sys
import os
from os.path import join
from time import sleep

## Initial setup
sys.path.append(os.path.abspath(join(os.getcwd(),'../..','common')))
import common
import core

import StateMachines
from transitions.core import MachineError

    
def add_paths():
    root = os.getcwd()
    if common.CDS.read('platform') == 'Linux':
        volatile = '/vol'
        config = '/configuration'
        common.Paths['DATABASE'] = '/media/data.db'
        
    else:
        volatile = root
        config = os.path.abspath(join(os.getcwd(),'../..','configuration'))
        common.Paths['DATABASE'] = join(root,'data.db')
   
    common.Paths['DEBUG_LOG'] = join(volatile,'debug.log')
    common.Paths['CONFIG'] = join(config, 'config.ini')
    common.Paths['CONFIG_SCHEMA'] = join(config, 'schema.ini')
    common.Paths['VERSION'] = join(config, 'version.json')
    common.Paths['VOLATILE'] = volatile
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger=logging.getLogger(__name__)
        
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
        try:
            logger.info('requesting transition')
            common.OpMode.next()
            while common.OpMode.state == curr_state:
                pass
        except MachineError as e:
            logger.error(e)
            break