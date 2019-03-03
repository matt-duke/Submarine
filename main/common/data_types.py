from time import time, sleep
from enum import Enum, auto
import logging
from threading import Thread

from self_test import verify_src_module

## Shared custom data types
class OpMode(Enum):
    none = 0
    startup = auto()
    test = auto()
    calibration = auto()
    normal = auto()
    emergency = auto()
    critical_fault = auto()

            
class Sensor:
    timeout = 30
    def __init__(self, name, type, logger, check_valid):
        self.logger = logger
        self.value = None
        self.type = type
        self.name = name
        self.valid = False
        self.timestamp = -1
        self.check_valid = check_valid
        
    def write(self, val):
        self.logger.debug('Writing value {}:{}'.format(self.name, val))
        self.value = self.type(val)
        self.timestamp = time()
        self.valid = True
        return self.valid
        
    def read(self):           
        if all([((time()-self.timestamp) > Sensor.timeout), self.check_valid]):
            self.valid = False
            self.logger.warning(self.name+': validity changed to false: time delta '+str(time()-self.timestamp))
        self.logger.debug('Reading value {}:{}'.format(self.name, self.value))
        return self.value
        
class Bus(dict):
    def __init__(self, name, config, platform):        
        dict.__init__(self)
        self.name = name
        self.platform = platform
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(config['LogLevel'])
        self.enabled = config['Enabled']
        self.refresh_rate = config['RefreshRate']
        module = config['Module']
        self.thread = Thread()
        try:
            class_name = "SrcClass"
            self.module = getattr(__import__(module, fromlist=[class_name]), class_name)(self)
            self.enabled = verify_src_module(self.module) and self.enabled
        except Exception as e:
            self.logger.error('Error importing: {}'.format(e))
            self.enabled = False
    
    def write(self, name, value):
        if name in self.keys():
            if not self[name].write(value):
                self.logger.error('Error writing to '+name)
            else:
                pass
        else:
            self.logger.error('Sensor:{} not initialized to {}.'.format(name, self.name))
    
    def add_sensor(self, name, **kwargs):
        if type(kwargs) == Sensor:
            self[name] = kwargs
        else:
            if 'check_valid' not in kwargs.keys():
                kwargs['check_valid'] = True
            try:
                self[name] = Sensor(name, kwargs['type'], self.logger, kwargs['check_valid'])
                self.logger.info('Adding sensor {}'.format(name))
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
            self.module.setup()
            self.thread.__init__(target=run, args=(self.module.loop,))
            self.logger.info('Starting {} thread'.format(self.name))
            self.thread.start()