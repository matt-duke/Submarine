import logging
logger = logging.getLogger(__name__)

def get_time():
    return None
    
def flatten(l):
    return [item for sublist in l for item in sublist]
    
def get_sensor(name, log=True):
    from common import BUS
    for bus in BUS:
        if name in bus.keys():
            return bus.get(name)
    if log:        
        logger.error('Sensor not found: '+name)