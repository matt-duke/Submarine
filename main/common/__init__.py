from common import data_types
from common.helper import flatten, get_sensor


## Managers
from common.BusManager import BusManager
BusManager = BusManager()


#Shared/common variables
log_dict = {"DEBUG": 10,
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50}
OpMode = None