from threading import Thread
import logging
from time import sleep

import src.config as config
from utility.rpi import gpio_init

def init():
    

def main(): 
    while True:
        print(config.sensor[0].value)
        sleep(1)
        
if __name__ == '__main__':
    init()
    main()
