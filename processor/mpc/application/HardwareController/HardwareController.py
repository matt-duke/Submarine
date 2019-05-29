import common
import core

from time import sleep
import random

# Import own objects from __init__ file
from . import *

class HardwareController(core.BaseClass):
    def __init__(self):
        core.BaseClass.__init__(self)
        self.Light = HardwareObjects.Light()
        self.Fan = HardwareObjects.Fan()
        self.Mcu = Mcu.McuClass()
        
    def monitor(self):
        def run():
            pass

        self.addThread('hwctrl_monitor',run,sleep=2).start()
        
    def update_sensors(self):
        def run():
            common.CDS.get('cpu_temp').write(random.randrange(25, 40))
            
        self.addThread('hwctrl_monitor',run,sleep=2).start()