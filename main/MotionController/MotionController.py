import logging
logger = logging.getLogger(__name__)

import common

#__name__ = 'MotionController'

class ControlAlgorithm:
    def __init__(self):
        self.prev
    def input(self, val1, val2):
        val = (val1+val2)/2
        self.prev = val
        return val
        
    
class MotionController(common.BaseClass):
    def __init__(self):
        common.BaseClass.__init__(self)

        
    