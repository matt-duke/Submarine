import common
import logging
from pathlib import Path 

import src

logger = logging.getLogger(__name__)

def start():
    logger.info('Setting up interfaces')
    
    print(dir(src))
    for mod in dir(src):
        #print(mod, type(getattr(src, mod)))
        if type(getattr(src, mod)) == type:
            common.BUS.append(getattr(src, mod))
            logger.info('Adding data bus: '+mod)
            
    #for bus in common.BUS:
     #   bus.start()