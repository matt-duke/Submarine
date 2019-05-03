import logging
from time import time

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