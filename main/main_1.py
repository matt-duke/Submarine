from threading import Thread
import config as c
from webpage import site
from utility import gpioInit, close
from comm import arduino_status
from time import sleep
import atexit

def test():
    while 1:
        sleep(.5)
        c.mode = "TRUE"
        print("test")


c.init()
gpioInit()


threads = []

threads[1] = Thread(target=site)
threads[2] = Thread(target=arduino_status)

for i in len(threads):
    threads[i].daemon = True
    threads[i].start()
    threads[i].join()

atexit.register(close)

