import os
import psutil
from pathlib import Path
from time import sleep
import shutil

import common
from common.data_types import Bus

class SrcClass(Bus):
    def __init__(self):
        Bus.__init__(self, "I2cMgr")
        self.add_sensor('batt_voltage', type=int, check_valid=False)
        self.add_sensor('depth', type=int, check_valid=False)
        self.add_sensor('pressure', type=int, check_valid=False)
        self.add_sensor('m1_current', type=int, check_valid=False)
        self.add_sensor('m2_current', type=int, check_valid=False)
        
    def setup(self):   
        self.write('batt_voltage', 5)
        self.write('depth', 20)
        self.write('pressure', 40)
        self.write('m1_current', 0)
        self.write('m2_current', 0)
    
    def loop(self):
        pass
    
    def connection_test(self):
        return True
