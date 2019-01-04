import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from common import sql
from common.config import Sensor
from common.config import OpMode

## Common variables
sensors = {}
mode = OpMode.none
config = {}