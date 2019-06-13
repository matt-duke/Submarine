from threading import Thread, Event, RLock
from queue import Queue
import subprocess
from subprocess import PIPE
import platform
import logging
import os


import time
import common



class BaseThread(Thread):
    def __init__(self, BaseSelf, name, fnc, args):
        Thread.__init__(self)
        self.name = name
        self.fnc = fnc
        self.args = args
        self.logger = BaseSelf.logger
        self.BaseSelf = BaseSelf
        self.kill_event = Event()
        self.output = Queue(maxsize=1)
    
    def kill(self, block=True):
        self.kill_event.set()
        if block:
            self.wait()
    
    def wait(self, timeout=10):
        self.kill_event.wait(timeout)
        while self.isAlive():
            pass
    
    def setup(self):
        #overwite function to add setup actions
        self.logger.info('Starting thread '+self.name)
    
    def start(self, sleep=0, loop=False):
        self.loop = loop
        self.sleep = sleep
        try:
            self.setup()
            Thread.start(self)
        except Exception as e:
            self.logger.critical('Exception starting thread {}: {}'.format(self.name, e))
    
    def run(self):
        out = None
        while True:
            if self.kill_event.is_set():
                self.logger.warning('Killing thread '+self.name)
                break
            else:
                try:
                    self.BaseSelf.lock.acquire()
                    out = self.fnc(*(self.BaseSelf, self)+self.args)
                    self.BaseSelf.lock.release()
                except Exception as e:
                    self.logger.critical('Thread {} crash: {}'.format(self.name, e))
                    self.kill_event.set()
            #quit loop if loop is not set
            if not self.loop:
                break
            time.sleep(self.sleep)
            
        self.output.put(out)
        self.logger.debug('Thread ending '+self.name)


class BaseClass:
    class ThreadManager(dict):
        def __init__(self, BaseSelf):
            dict.__init__(self)
            self.BaseSelf=BaseSelf
        
        def add(self, name, fnc, args=()):
            thread = BaseThread(self.BaseSelf, name=name, fnc=fnc, args=args)
            i = 0
            for key in self.keys():
                if name == key:
                    i+=1
            if i > 0:
                name = '{}_{}'.format(name, i)
            self[name] = thread
            return thread
    
        def killAll(self, block=True):  
            for key, thread in self.items():
                thread.kill()
                if block:
                    thread.wait()
                
    def __init__(self):
        self.threads = dict()
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        self.lock = RLock()
        self.threads = self.ThreadManager(self)
        
    def fileExists(self, path):
        if not os.path.exists(path):
            self.logger('File does not exist: {}'.format(path))
            return False
        return True
    
            
    def systemCall(self, cmd, block=True):
        # non-blocking runs in thread

        self.logger.debug('Running command: '+ ''.join(cmd))
        def __run(self, threadSelf):
            CmpPr = subprocess.run(cmd, stdout=PIPE, stderr=PIPE)
            self.logger.debug(CmpPr.stdout)
            if CmpPr.returncode == 0:
                self.logger.debug(CmpPr.stderr)
            else:
                self.logger.error('Non-zero return code in systemCall. stderr: "{}"'.format(CmpPr.stderr))
                
            return CmpPr.returncode
        
        thread = self.threads.add('nb_systemCall', __run)
        thread.start()
        if block:
            thread.wait()
        return thread.output.get()
        
