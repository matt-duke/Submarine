from threading import Thread
import logging
from time import sleep

import src.config as config
from src.utility import gpio_init

def main():
    gpio_init()

    threads = []
    #threads[1] = Thread(target=site)
    #threads[2] = Thread(target=arduino_status)

    #for i in len(threads):
    #    threads[i].daemon = True
    #    threads[i].start()
    #    threads[i].join
        
if __name__ == '__main__':
    config.var_init()
    logging.basicConfig(level=logging.INFO)
    if config.debug:
        logging.basicConfig(filename = 'debug.log', filemode ='w', level=logging.DEBUG)
    main()
