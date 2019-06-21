import configparser
import os
from os.path import join
import logging
from logging.handlers import RotatingFileHandler
import tarfile

import multiprocessing

import common
import core

from . import *

class MpcController(core.BaseClass):
    def __init__(self):
        core.BaseClass.__init__(self)
        self.POST = POST.PostClass()
          
    def import_config():
        common.config = configparser.ConfigParser()
        common.config.read(common.Paths['CONFIG'])
    
    def update(self, file):
        if not self.fileExists(file):
            self.logger.warning('Update failed')
            return False
        try:
            tarfile.TarFile.open(file)
            tarfile.extract('expected_sw_config.json', common.Paths['VERSION'])
            tarfile.extract('uboot', common.Paths['UBOOT'])
        except Exception as e:
            self.logger.error(e)
        
    def os_update(self):
        if self.wan(): 
            self.systemCall('sudo apt update -y')
            self.systemCall('sudo apt upgrade -y')
            self.systemCall('sudo apt autoremove -y')
        else:
            self.logger.error('WAN not connected')
