from threading import Thread
import config as c
import utility as u
import logger
from time import sleep

c.init()
u.gpioInit()


threads = []

threads[1] = Thread(target=site)
threads[2] = Thread(target=arduino_status)

for i in len(threads):
    threads[i].daemon = True
    threads[i].start()
    threads[i].join()

