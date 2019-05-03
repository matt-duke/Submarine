import subprocess as sp
import os
import configparser

import common
from .verify_config_file import verify_config_file
import logging
import logging.handlers

logger = logging.getLogger(__name__)

class Setup(common.BaseClass):
    def __init__(self):
        common.BaseClass.__init__(self)
        
    def check_software(self):
        sp.run(['git,-v'])
    
    def update(self):
        if not self.wan_access():
            return False
        try:
            sp.run(['apt-get','update'], check=True)
            sp.run(['apt-get','upgrade'], check=True)
            sp.run(['git','pull','origin','build'], check=True)
            #run git setup script
            arduino_version = 1.0
            if common.CDS.get('arduino_version') < arduino_version:
                sp.run(['arduino','file'])
            sp.run(['reboot'])
        except Exception as e:
            logger.error('Update failed due to: {}'.format(e))
            return False
            
    def update_datetime(self):
        pass
    
    def import_configuration(self):
        config = configparser.ConfigParser()
        config.read(os.path.join('configuration','config.ini'))
        verify_config_file(config)
        return config
        
    def start_logging(self):
        log_level_dict = {'CRITICAL':50,
                          'ERROR':40,
                          'WARNING':30,
                          'INFO':20,
                          'DEBUG':10,
                          'NOTSET':0}
    
        rootLogger = logging.getLogger()
        for hdlr in rootLogger.handlers:
            rootLogger.removeHandler(hdlr)
        
        class CriticalHandler(logging.Handler):
            def __init__(self):
                logging.Handler.__init__(self)
                self.setLevel(logging.CRITICAL)
            def emit(self, record):
                common.OpMode.to_critical()

        modeHandler = CriticalHandler()
        rootLogger.addHandler(modeHandler)
        
        logFormatter = logging.Formatter(common.config['LOGGER']['Format'], 
                                         common.config['LOGGER']['DateFormat'])
        RotatingFileHandler = logging.handlers.RotatingFileHandler
        fileHandler = RotatingFileHandler(common.Paths['DEBUG_LOG'],
                                          maxBytes=10*1024*1024,
                                          backupCount=2)
        fileHandler.setLevel(log_level_dict[common.config.get('LOGGER','FileLogLevel')])
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        consoleHandler.setLevel(log_level_dict[common.config.get('LOGGER','StreamLogLevel')])
        rootLogger.addHandler(consoleHandler)
        