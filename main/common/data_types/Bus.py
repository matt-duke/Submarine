from time import time, sleep
import logging
from threading import Thread
import common

class Bus(dict):
    def __init__(self, name):
        dict.__init__(self)
        self.name = name
        
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(20)
        self.enabled = True
        self.refresh_rate = 1
        self.thread = Thread()
    
    def setup(self):
        return None
    
    def loop(self):
        return None
    
    def write(self, name, value):
        if name in self.keys():
            if not self[name].write(value):
                self.logger.error('Error writing to '+name)
            else:
                pass
        else:
            self.logger.error('Sensor:{} not initialized to {}.'.format(name, self.name))
    
    def add_sensor(self, name, **kwargs):
        if type(kwargs) == common.data_types.Sensor:
            self[name] = kwargs
        else:
            if 'check_valid' not in kwargs.keys():
                kwargs['check_valid'] = True
            try:
                self[name] = common.data_types.Sensor(name, kwargs['type'], self.logger, kwargs['check_valid'])
                self.logger.info('Adding sensor {}'.format(name))
            except Exception as e:
                self.logger.error('Error adding sensor to {}.Error: {}'.format(self.name, e))
    
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