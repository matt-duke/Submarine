import logging
logger = logging.getLogger(__name__)

import common

class InterfaceManager(common.BaseClass):
    def __init__(self):
        common.BaseClass.__init__(self)
        self.bus = dict()
        
    def importSrc(self):
        from . import Sim
        self.bus['Sim'] = Sim.SrcClass()
        
    def startAll(self):
        for key,bus in self.bus.items():
            bus.start()
            
    def testAll(self):
        result = True
        for key,bus in self.bus.items():
            result &= bus.test()
        return result