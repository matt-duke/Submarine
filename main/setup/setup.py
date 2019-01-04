import common
import logging
logger = logging.getLogger(__name__)

from setup.config_parser import config_parser

def run():
    ## By the end of this function, all startup items should be done.
    ## Includes initializing sensors, parsing config file(s), network details, tests, etc.
    common.mode = common.OpMode.startup
    common.config = config_parser('setup/config.ini')
    common.Sensor.timeout = common.config.getint('SENSOR','ValidityTimeout')
    start_logging()
    
def start_logging(): 
    logFormatter = logging.Formatter(common.config['LOGGER']['Format'], 
                                     common.config['LOGGER']['DateFormat'])
    rootLogger = logging.getLogger()
    rootLogger.setLevel(common.log_dict[common.config['LOGGER']['LogLevel']])
    fileHandler = logging.FileHandler(common.config['LOGGER']['FileName'])
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    
    logging.basicConfig(level = log_dict[common.config['LOGGER']['LogLevel']],
                        filename = common.config['LOGGER']['FileName'],
                        filemode = 'w',
                        format = common.config['LOGGER']['Format'])
    logging.getLogger('werkzeug').setLevel('WARNING')


def start_network():
    pass