import common
import core


class ControlAlgorithm:
    def __init__(self):
        self.prev
    def input(self, val1, val2):
        val = (val1+val2)/2
        self.prev = val
        return val
        
    
class MotionController(core.BaseClass):
    def __init__(self):
        core.BaseClass.__init__(self)

        
    