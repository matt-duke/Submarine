from threading import Thread
import logging
from time import sleep

import src.config as config
from utility.rpi import gpio_init
from src.comm import I2c

def main():
    gpio_init()
    mcu = I2c()
    
    threads = []
    threads.append(Thread(target=mcu.connect))

    for t in threads:
        t.setDaemon(True)
        t.start()
        
    while True:
        print(config.sensor[0].value)
        sleep(1)
        
if __name__ == '__main__':
    config.var_init()
    main()
