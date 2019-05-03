import logging
logger = logging.getLogger(__name__)
import common

def get_time():
    return None
    
def flatten(l):
    return [item for sublist in l for item in sublist]
    
def get_sensor(name, log=True):
    if log:        
        logger.error('Sensor not found: '+name)
