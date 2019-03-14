import os
import psutil
from pathlib import Path
from time import sleep
import shutil

import common

class SrcClass(common.data_types.Bus):
    def __init__(self):
        common.data_types.Bus.__init__()
        self.bus.add_sensor('batt_voltage', type=int, check_valid=False)
        self.bus.add_sensor('depth', type=int, check_valid=False)
        self.bus.add_sensor('pressure', type=int, check_valid=False)
        self.bus.add_sensor('m1_current', type=int, check_valid=False)
        self.bus.add_sensor('m2_current', type=int, check_valid=False)
        
    def setup(self):   
        self.bus.write('batt_voltage', 5)
        self.bus.write('depth', 20)
        self.bus.write('pressure', 40)
        self.bus.write('m1_current', 0)
        self.bus.write('m2_current', 0)
    
    def loop(self):
        pass
    
    def test(self):
        pass
