from threading import Thread
import logging
from time import sleep

import src.config as config
from src.utility import gpio_init
from src.comm import start_i2c_read

def main():
    gpio_init()

    threads = []
    threads.append(Thread(target=start_i2c_read))

    for t in threads:
        t.setDaemon(True)
        t.start()
        
    while True:
        print(config.sensor[0].value)
        sleep(1)
        
if __name__ == '__main__':
    config.var_init()
    main()
