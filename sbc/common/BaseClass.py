from threading import Thread, Event
from queue import Queue

import logging
logger = logging.getLogger(__name__)

import time

class BaseThread(Thread):
    def __init__(self, name, fnc, args, sleep):
        Thread.__init__(self)
        self.name = name
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
    def __init__(self, name=""):
        self.threads = dict()
        
    def addThread(self, name, fnc, args=(), sleep=1):
        thread = BaseThread(name, fnc, args, sleep)
        self.threads[name] = thread
        return thread
        
    def closeThread(self, key, block=False):
        if key in self.threads.keys():
            self.thread[key].kill()
            while self.thread[key].isAlive():
                pass
            del self.thread[key]
            logger.info('Thread killed: '+key)
        else:
            logger.error('Thread '+key+' not found')
        
    def closeAllThreads(self, block=False):
        for key, thread in self.threads.items():
            self.closeThread(block)