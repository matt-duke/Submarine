import common
import logging
import os
from logging.handlers import RotatingFileHandler
logger = logging.getLogger(__name__)

consoleHandler = logging.StreamHandler()
logging.getLogger().setLevel(0)
logging.getLogger().addHandler(consoleHandler)

from setup.config_parser import config_parser
import self_test

def run():
    ## By the end of this function, all startup items should be done.
    ## Includes initializing sensors, parsing config file(s), network details, tests, etc.
    common.mode = common.OpMode.startup
    self_test.run_post()
    
    common.config = config_parser('config.ini')
    self_test.verify_config_file(common.config)
    
    start_logging()
    
def start_logging():
    rootLogger = logging.getLogger()
    for hdlr in rootLogger.handlers:
        rootLogger.removeHandler(hdlr)
    
    class CriticalHandler(logging.Handler):
        def __init__(self):
            logging.Handler.__init__(self)
            self.setLevel(logging.CRITICAL)
        def emit(self, record):
            common.mode = common.OpMode.critical_fault

    modeHandler = CriticalHandler()
    rootLogger.addHandler(modeHandler)
    
    if os.path.isfile(common.config['LOGGER']['FileName']):
        os.remove(common.config['LOGGER']['FileName'])
    
    logFormatter = logging.Formatter(common.config['LOGGER']['Format'], 
                                     common.config['LOGGER']['DateFormat'])
    fileHandler = RotatingFileHandler(common.config['LOGGER']['FileName'],
                                      maxBytes=10*1024*1024,
                                      backupCount=2)
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
