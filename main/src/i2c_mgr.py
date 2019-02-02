import os
import psutil
from pathlib import Path
from time import sleep
import shutil

import common

class SrcClass():
    def __init__(self, bus):
        self.bus = bus
        self.logger = bus.logger
        
    def setup(self):
        self.bus.add_sensor('batt_voltage', type=int, check_valid=False)
        self.bus.add_sensor('depth', type=int, check_valid=False)
    
        self.bus.write('batt_voltage', 5)
        self.bus.write('depth', 20)
    
    def loop(self):
        pass
    
    def test(self):
        pass
