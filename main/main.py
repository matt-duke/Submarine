from threading import Thread
import logging
from time import sleep, time
import os
import shutil
import utility.map as map

import src.config as config
from src.comm import I2c
from utility.rpi import gpio_init
from server import start_server

def thread_test(id, delay=1):
    start = time()
    while True:
        sleep(delay)
        print('Main thread timing accuracy: {:.4f}s'.format(time()-start-delay))
        start = time()
    
def start():
    config.init()
    config.init_db()
    gpio_init()
    
    mcu = I2c()
    threads = []
    threads.append(Thread(target=thread_test, args=(0,5)))
    for t in threads:
        t.setDaemon(True)
        t.start()
    
        
if __name__ == '__main__':
    start()
    stream()
    socket()
