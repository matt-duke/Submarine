from threading import Thread, Event
from queue import Queue
import subprocess as sp
import platform
import logging


import time
import common

class BaseThread(Thread):
    def __init__(self, name, fnc, args, sleep, logger):
        Thread.__init__(self)
        self.name = name
        self.logger = logger
        self.fnc = fnc
        self.args = args
        self.sleep = sleep
        self.kill_event = Event()
        
    def kill(self):
        self.kill_event.set()
           
    def run(self):
        logger.info('Starting thread '+self.name)
        while True:
            if self.kill_event.is_set():
                logger.warning('Killing thread '+self.name)
                break
            else:
                if self.args == ():
                    self.fnc()
                else:
                    self.fnc(self.args)
            time.sleep(self.sleep)
            

class BaseClass:
    def __init__(self):
        self.threads = dict()
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        
    def addThread(self, name, fnc, args=(), sleep=1):
        thread = BaseThread(name, fnc, args, sleep, logger=self.logger)
        self.threads[name] = thread
        return thread
        
    def closeThread(self, key, block=True):
        if key in self.threads.keys():
            self.thread[key].kill()
            while self.thread[key].isAlive():
                pass
            del self.thread[key]
            self.logger.info('Thread killed: '+key)
        else:
            self.logger.error('Thread '+key+' not found')
        
    def fileExists(self, path):
        if not os.path.exists(path):
            self.logger('File does not exist: {}'.format(path))
            return False
        return True
    
    def closeAllThreads(self, block=True):
        for key, thread in self.threads.items():
            self.closeThread(block)
            
    def systemCall(self, cmd):
        CmpPr = subprocess.run(cmd, capture_output=True)
        self.logger.debug(CmpPr.stdout)
        if CmpPr.returncode > 0:
            self.logger.error('Non-zero return code in systemCall. stderr: {}'.format(Cmp.stderr))
            return False
        else:
            return True
