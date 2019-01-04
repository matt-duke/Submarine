from time import time
from enum import Enum, auto

import common.sql as sql
from common import logger
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
    timeout = 10
    type_map = [int, float, str]
    def __init__(self, type=None, check_valid=True):
        self.value = None
        self.type = type
        self.valid = False
        self.timestamp = -1
        self.check_valid = check_valid
        
    def write(self, val):
        try:
            self.value = Sensor.type_map[self.type](val)
            self.valid = True
        except Exception as e:
            self.valid = False
            print(e)
        self.timestamp = time()
        return self.valid
        
    def read(self, do_not_update=False):
        if do_not_update:
            return self.value
        if (time()-self.timestamp) > Sensor.timeout and self.check_valid:
            self.valid = False
            print('Label validity changed to false')
        return self.value