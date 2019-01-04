from common import sql
from common.config import Sensor
from common.config import OpMode

## Common variables
sensors = {}
mode = OpMode.none
config = {}
log_dict = {"DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL}
    