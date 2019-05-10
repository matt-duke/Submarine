import common
from . import HardwareObjects
from time import sleep
import random

__name__ = 'HardwareController'

class HardwareController(common.BaseClass):
    def __init__(self):
        self.Light = HardwareObjects.Light()
        self.Fan = HardwareObjects.Fan()
        common.BaseClass.__init__(self, __name__)
        
    def monitor(self):
        def run():
            pass

        self.addThread('hwctrl_monitor',run,sleep=2).start()
        
    def update_sensors(self):
        def run():
            common.CDS.get('cpu_temp').write(random.randrange(25, 40))