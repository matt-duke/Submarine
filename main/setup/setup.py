import common
import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger(__name__)

from setup.config_parser import config_parser

def run():
    ## By the end of this function, all startup items should be done.
    ## Includes initializing sensors, parsing config file(s), network details, tests, etc.
    common.mode = common.OpMode.startup
    common.config = config_parser('config.ini')
    common.Sensor.timeout = common.config.getint('SENSOR','ValidityTimeout')
    start_logging()
    
def start_logging():
    class CriticalHandler(logging.Handler):
        def __init__(self):
            logging.Handler.__init__(self)
            self.setLevel(logging.CRITICAL)
        def emit(self, record):
            common.mode = common.OpMode.critical_fault
            
    rootLogger = logging.getLogger()
    rootLogger.setLevel(0)
    modeHandler = CriticalHandler()
    rootLogger.addHandler(modeHandler)
    rootLogger.critical('BAD')
    
    logFormatter = logging.Formatter(common.config['LOGGER']['Format'], 
                                     common.config['LOGGER']['DateFormat'])
    fileHandler = RotatingFileHandler(common.config['LOGGER']['FileName'],
                                      maxBytes=200*1024,
                                      backupCount=2,
                                      mode='w')
    fileHandler.setLevel(common.log_dict[common.config['LOGGER']['FileLogLevel']])
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(common.log_dict[common.config['LOGGER']['StreamLogLevel']])
    rootLogger.addHandler(consoleHandler)
    
    greylist = ['werkzeug', 'engineio', 'socketio']
    for name in greylist:
        logging.getLogger(name).setLevel('WARNING')


def start_network():
    pass
