import configparser
import os
from os.path import join
import logging
from logging.handlers import RotatingFileHandler

import common
import core

from . import *

class MpcController(core.BaseClass):
    def __init__(self):
        core.BaseClass.__init__(self)
        self.POST = POST.PostClass()
    
    def setup(self):        
        def __import_config():
            common.config = configparser.ConfigParser()
            common.config.read(common.Paths['CONFIG'])
        
        def __configureRootLogger():
            rootLogger = logging.getLogger()
            for hdlr in rootLogger.handlers:
                rootLogger.removeHandler(hdlr)        

            logFormatter = logging.Formatter(common.config['LOGGER']['Format'], 
                                         common.config['LOGGER']['DateFormat'])

            fileHandler = RotatingFileHandler(common.Paths['DEBUG_LOG'],
                                          maxBytes=10*1024*1024,
                                          backupCount=2)
                                          
            fileHandler.setLevel(common.config['LOGGER']['FileLogLevel'])
            logFormatter = logging.Formatter(common.config['LOGGER']['Format'])
            fileHandler.setFormatter(logFormatter)
            rootLogger.addHandler(fileHandler)
            
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(core.Logger.ColoredFormatter(common.config['LOGGER']['Format']))
            consoleHandler.setLevel(common.config['LOGGER']['StreamLogLevel'])
            rootLogger.addHandler(consoleHandler)
            
            greylist = ['werkzeug', 'engineio', 'socketio', 'transitions']
            for name in greylist:
                logging.getLogger(name).setLevel('WARNING')
    
            
        __import_config()
        __configureRootLogger()
        
    def update(self, file):
        pass
    def os_update(self):
        pass
