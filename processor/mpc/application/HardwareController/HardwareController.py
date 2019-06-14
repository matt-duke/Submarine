import common
import core

import os
from time import sleep
import random

from . import *

class HardwareController(core.BaseClass):
    def __init__(self):
        core.BaseClass.__init__(self)
        self.Light = HardwareObjects.Light()
        self.Fan = HardwareObjects.Fan()
        self.Mcu = Mcu.McuClass('/dev/ttyACM0')
    
    def monitor(self):
        def __run():
            pass

        #self.threads.add('hwctrl_monitor',__run, sleep=2, loop=True).start()
        
    def update_sensors(self):
        def __run():
            common.CDS.get('cpu_temp').write(random.randrange(25, 40))
            
        self.threads.add('hwctrl_update',__run, loop=True, sleep=2).start()
        
    def update_mcu(self, dir):
        if common.testmode:
            logger.warning('Unable to flash MCU in testmode')
            return
            
        dir='/tmp/update/build-mega2560'
        self.Mcu.upload(os.path.join(dir, 'update.hex'))
        
    def mcu_test(self):
        self.Mcu.connect()
        msg = b'\x00\x00\x00\x00'
        resp = self.Mcu.write(msg)
        return resp == msg