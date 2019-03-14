from common.data_types import Sensor
from common.data_types import OpMode

from common import bus_mgr

from common.helper import flatten, get_sensor

from common import sql

## Common variables
BUS = []
MODE = OpMode.none
config = {}
PLATFORM = None

#log level dictionary corresposding to logging.DEBUG to logging.CRITIAL levels
log_dict = {"DEBUG": 10,
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50}
        