from time import time
from enum import Enum, auto
import logging
from threading import Thread

import common

## Shared custom data types
class OpMode(Enum):
    none = 0
    startup = auto()
    test = auto()
    calibration = auto()
    normal = auto()
    emergency = auto()
    critical_fault = auto()

class Bus(dict):
    def __init__(self, name, config):        
        dict.__init__(self)
        
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(config['LogLevel'])
        self.enabled = config['Enabled']
        self.package = config['Path']
        self.thread = Thread()
        
        class_name = "run"
        try:
            import src.hw_mgr.SrcClass
            print(__import__(self.package))
            #thread.start()
        except Exception as e:
            self.logger.error('Error starting thread:{}'.format(e))
    
    def add_sensor(self, name, type, check_valid):
        self[name] = Sensor(name, type, self.logger, check_valid)
    
    def run(self):
        if not self.thread.isAlive and self.enabled:
            pass
            
            
class Sensor:
    timeout = 5
    type_map = [int, float, str]
    def __init__(self, name, type, logger, check_valid):
        self.logger = logger
        self.value = None
        self.type = type
        self.name = name
        self.valid = False
        self.timestamp = -1
        self.check_valid = check_valid
        
    def write(self, val):
        try:
            self.value = Sensor.type_map[self.type](val)
            self.valid = True
            self.logger.debug('Writing value {}:{}'.format(self.name, val))
        except Exception as e:
            self.valid = False
            self.logger.error(e)
        self.timestamp = time()
        return self.valid
        
    def read(self, do_not_update=False):
        if not do_not_update and (time()-self.timestamp) > Sensor.timeout and self.check_valid:
            self.valid = False
            self.logger.warning('Label validity changed to false')
        self.logger.debug('Reading value {}:{}'.format(self.name, self.value))
        return self.value