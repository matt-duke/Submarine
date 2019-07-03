import json
import logging

logger = logging.getLogger(__name__)

default = None
default.is_valid = False

def load(file = 'defaults.json'):
    default = json.load(open(file, 'r'))
    default.is_valid = verify(default)
    
def get():
    if default == None:
        load()
    if not default.is_valid:
        logger.error("{} is not valid".format(file))
        
    return default
