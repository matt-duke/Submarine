from time import time
from enum import Enum, auto
import logging
logger = logging.getLogger(__name__)

import common
import setup

## Shared custom data types
class OpMode(Enum):
    none = 0
    startup = auto()
    test = auto()
    calibration = auto()
    normal = auto()
    emergency = auto()
    error = auto()

class Sensor:
    timeout = 5
    log
    type_map = [int, float, str]
    def __init__(self, name, type, check_valid):
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
            logger.debug('Writing value {}:{}'.format(self.name, val))
        except Exception as e:
            self.valid = False
            logger.error(e)
        self.timestamp = time()
        return self.valid
        
    def read(self, do_not_update=False):
        if not do_not_update and (time()-self.timestamp) > Sensor.timeout and self.check_valid:
            self.valid = False
            print('Label validity changed to false')
        logger.debug('Reading value {}:{}'.format(self.name, self.value))
        return self.value