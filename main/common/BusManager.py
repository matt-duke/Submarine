import logging
from pathlib import Path 

import src

logger = logging.getLogger(__name__)

class BusManager():
    bus_list = []
    
    def add_interfaces(self):
        logger.info('Setting up interfaces')
        
        for mod in dir(src):
            attr = getattr(src, mod)
            if type(getattr(src, mod)) == type:
                if self.verify_src_module(attr):
                    self.bus_list.append(attr())
                    logger.info('Added data bus: '+mod)
                else:
                    logger.error('Failed to add {}'.format(mod))
                
    def list(self):
        return self.bus_list
        
    def verify_src_module(self, module, modules=[]):
        result = True
        expected = ['setup','loop','connection_test']+modules
        for e in expected:
            if not hasattr(module, e):
                result = False
                logger.error('Missing module: {}'.format(e))
        return result