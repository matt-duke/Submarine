from time import time, sleep
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
        self.refresh_rate = config['RefreshRate']
        module = config['Module']
        self.thread = Thread()
        
        try:
            class_name = "SrcClass"
            self.module = getattr(__import__(module, fromlist=[class_name]), class_name)(self)
            self.enabled = common.self_test.verify_src_module(self.module) and self.enabled
        except Exception as e:
            self.logger.error('Error importing: {}'.format(e))
            self.enabled = False
    
    def write(self, name, value):
        if name in self.keys():
            self[name].write(value)
        else:
            self.logger.error('Sensor:{} not initialized to {}. Check config.ini'.format(name, self.name))
    
    def add_sensor(self, name, **kwargs):
        if type(kwargs) == Sensor:
            self[name] = kwargs
        else:
            try:
                self[name] = Sensor(name, kwargs['type'], self.logger, kwargs['check_valid'])
            except Exception as e:
                self.logger.error('Error adding sensor to {}. Check {}'.format(self.name, e))
    
    def start(self):
        def run(func):
            while True:
                start_time = time()
                func()
                end_time = time()
                sleep(self.refresh_rate)
        
        if not self.thread.isAlive() and self.enabled:
            self.logger.info('Starting {} thread'.format(self.name))
            self.module.setup()
            self.thread.target = run
            self.thread.args = (self.module.loop,)
            self.thread.start()

            
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