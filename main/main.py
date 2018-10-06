from config import *
from webpage import site
from threading import Thread
import time

def test2():
    while 1:
        print(sensor[1].value)
        time.sleep(.5)

t1 = Thread(target=site)
t2 = Thread(target=test2)
t1.setDaemon(True)
t2.setDaemon(True)
t1.start()
t2.start()
while True:
    pass
