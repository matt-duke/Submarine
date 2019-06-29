from threading import Thread, Event, RLock
from queue import Queue
import platform
import logging
import os
import types
import traceback
import subprocess

import time
import common
        
        
class CustomLock:
    def __init__(self):
        self._lock = RLock()

    def acquire(self, timeout=5):
        self._lock.acquire(timeout)

    def release(self):
        self._lock.release()
        
    def __enter__(self):
        self.acquire()
        
    def __exit__(self, type, value, traceback):
        self.release()

class BaseThread(Thread):
    def __init__(self, BaseSelf, name, fnc, args):
        Thread.__init__(self)
        self.name = name
        self.fnc = fnc
        self.args = args
        #change later?
        self.daemon = True
        #print(type(BaseSelf.logger))
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
    
    def start(self, sleep=0, loop=False, timeout=100):
        self.loop = loop
        self.sleep = sleep
        self.timeout = timeout+time.time()
        try:
            self.setup()
            Thread.start(self)
        except Exception as e:
            self.logger.critical('Exception starting thread {}: {}'.format(self.name, e))
            traceback.print_exc()
    
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
                    traceback.print_exc()
                    self.kill_event.set()
            #quit loop if loop flag is not set
            if not self.loop:
                break
            time.sleep(self.sleep)
            
        self.output.put(out)
        self.logger.debug('Thread ending '+self.name)

class ThreadManager(dict):
    def __init__(self, BaseSelf):
        if 'name' not in dir(BaseSelf):
            BaseSelf.name = 'undefined_thread_mgr'
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

class BaseClass:
    def __init__(self):
        self.threads = dict()
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        self.lock = CustomLock()
        self.threads = ThreadManager(self)
        
        self.__fn_queue = Queue()
    
    def function_processor(self):
        def __run(self, ThreadSelf):
            fn_t = self.__fn_queue.get()
            self.lock.acquire()
            fn_t[0](*fn_t[1])
            self.lock.release
        self.threads.add(__run).start(loop=True)
    
    def register(self, fn):
        try:
            fn = gettattr(self, fn.__name__)
        except AttributeError:
            self.logger.error("Function not found: {}".format(fn.__name__))
        def __fn(*args):
            self.__fn_queue.add((fn, (*args)))
        
        
    def fileExists(self, path):
        if not os.path.exists(path):
            self.logger('File does not exist: {}'.format(path))
            return False
        return True
    
    def wan(self):
        return self.systemCall('ping 8.8.8.8 -c 1') == 0
    
    def wait(self, condition, timeout=5):
        timeout=-1 if timeout == None else timeout
        end_time = time.time()+timeout
        while condition() == False:
            if time.time() > end_time and timeout>0:
                self.logger.error('Wait timed out')
                return False
        return True
    
    def systemCall(self, cmd, block=True):
        # non-blocking runs in thread

        self.logger.debug('Running command: '+ ''.join(cmd))
        if type(cmd) == str:
            cmd = cmd.split(' ')
        def __run(self, threadSelf, cmd):
            CmpPr = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.logger.debug(CmpPr.stdout)
            if CmpPr.returncode == 0:
                self.logger.debug(CmpPr.stderr)
            else:
                self.logger.error('Non-zero return code in systemCall. stderr: "{}"'.format(CmpPr.stderr))
                
            return CmpPr
        
        thread = self.threads.add('systemCall', __run, (cmd,))
        thread.start()
        if block:
            thread.wait()
            return thread.output.get()
        else:
            return
