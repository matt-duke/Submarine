from threading import Thread
import common
from time import sleep
from utility import rpi

import logging
logger = logging.getLogger(__name__)

REFRESH_RATE = 0.1
MAX_FAILURE = 5



def FAN_FUNC(x):
    y = 0.01*(x-20)
    return y
    
class Monitor(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.error_count = 0
        
    def run(self):
        while True:
            if common.MODE == '':
                continue
            try:
                self.error_count = 0
            except Exception as e:
                if self.error_count < MAX_FAILURE:
                    logger.error('Monitor error: {}'.format(repr(e)))
                elif self.error_count == MAX_FAILURE:
                    logger.critical('Continuous monitoring critical failure')
                self.error_count += 1
            
            sleep(REFRESH_RATE)

InternalMonitor = Monitor()            