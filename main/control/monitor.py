from threading import Thread
import common
from time import sleep
from control import rpi

import logging
logger = logging.getLogger(__name__)

REFRESH_RATE = 0.1

def FAN_FUNC(x):
    y = 0.01*(x-20)
    return y
    
class Monitor(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.error_count = 0
        
    def run(self):
        while True:
            try:
                cpu_temp = common.get_sensor('cpu_temp')
                if cpu_temp.valid:
                    rpi.set_fan(FAN_FUNC(cpu_temp.read()))
                    
                m1_current = common.get_sensor('m1_current')
                if m1_current.valid:
                    pass
                    
                m2_current = common.get_sensor('m2_current')
                if m2_current.valid:
                    pass
                 
                self.error_count = 0
            except Exception as e:
                if self.error_count < 3:
                    logger.error('Monitor error: {}'.format(repr(e)))
                elif self.error_count == 3:
                    logger.critical('Continuous monitoring failure reported')
                self.error_count += 1
            
            sleep(REFRESH_RATE)
                