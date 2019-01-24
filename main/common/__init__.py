from common.data_types import Sensor
from common.data_types import OpMode
from common.data_types import Bus

from common.helper import flatten

from common.self_test import *

from common import sql

## Common variables
bus = []
mode = OpMode.none
config = {}
#log level dictionary corresposding to logging.DEBUG to logging.CRITIAL levels
log_dict = {"DEBUG": 10,
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50}
    