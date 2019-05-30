from threading import Thread, Event, Lock
from queue import Queue
import subprocess
from subprocess import PIPE
import platform
import logging
import os


import time
import common


class BaseThread(Thread):
    def __init__(self, BaseClassSelf, name, fnc, args, sleep, loop):
        Thread.__init__(self)
        self.name = name
        self.fnc = fnc
        self.args = args
        self.logger = BaseClassSelf.logger
        self.BaseClassSelf = BaseClassSelf
        self.sleep = sleep
        self.kill_event = Event()
        self.output_queue = Queue(maxsize=1)
        self.loop = loop
        self.lock = Lock()
    
    def kill(self):
        self.kill_event.set()
    
    def start(self):
        Thread.start(self)
        return self
    
    def run(self):
        self.logger.info('Starting thread '+self.name)
        output = None
        while True:
            if self.kill_event.is_set():
                self.logger.warning('Killing thread '+self.name)
                break
            else:
                try:
                    self.lock.acquire()
                    output = self.fnc(*(self.BaseClassSelf, self)+self.args)
                    self.lock.release()
                except Exception as e:
                    self.logger.critical('Thread {} crash: {}'.format(self.name, e))
                    self.kill_event.set()
            #quit loop if loop is not set
            if not self.loop:
                break
            time.sleep(self.sleep)
        self.output_queue.put(output)


class BaseClass:
    def __init__(self):
        self.threads = dict()
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        
    def addThread(self, name, fnc, args=(), loop=False, sleep=1):
        thread = BaseThread(self, name=name, fnc=fnc, args=args, loop=loop, sleep=sleep)
        i = 0
        for key in self.threads.keys():
            if name == key:
                i+=1
        if i > 0:
            name = '{}_{}'.format(name, i)
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
            
    def waitForThread(self, thread, timeout=60):
        if type(thread) == str:
            if thread in self.threads.key():
                thread = self.threads[thread]
            else:
                self.logger.error('Thread "{}" does not exist')
                return
        elif type(thread) != BaseThread:
            output = self.logger.error('Thread type must be BaseThread')
            return
            
        while thread.is_alive():
            pass
            
        output = thread.output_queue.get(block=True, timeout=None)
        del self.threads[thread.name]
        return output
        
    def fileExists(self, path):
        if not os.path.exists(path):
            self.logger('File does not exist: {}'.format(path))
            return False
        return True
    
    def closeAllThreads(self, block=True):
        for key, thread in self.threads.items():
            self.closeThread(block)
            
    def systemCall(self, cmd, blocking=True):
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
        
        thread = self.addThread('nb_systemCall', __run).start()
        if blocking:
            return self.waitForThread(thread)
