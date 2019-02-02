import common

from time import time, sleep
from threading import Thread
from queue import Queue

class I2c():
    def __init__(self):
        self.db_q = Queue()
        target = [self.connect, self.db_manager]
        for trg in target:
            t = Thread(target = trg)
            t.daemon = True
            t.start()
    
    def connect(self):
        adr = common.config['ARDUINO']['I2CAddress']
        while True:
            if not config.debug[1]:
                from smbus import SMBus
                bus = SMBus(1)
            
                bus.write_byte(adr, 0x09) # trigger send data
                r = bus.read_byte(adr)
                for i in range(r):
                    r = bus.read_byte(adr)
                    print(r)
                #config.sensor[0].value = r[2]
                sleep(5)

            else:
                config.sensor[0].value = -1
                self.db_q.put({"sensor_id": 0, "value": config.sensor[0].value})
                sleep(20)
                config.sensor[0].value = 1
                self.db_q.put({"sensor_id": 0, "value": config.sensor[0].value})
                sleep(20)
    
    def db_manager(self):
        while True:
            config.data_db.add_row(self.db_q.get())
            self.db_q.task_done()

    def write_value(self, msg):
        start = time()
        while self.send != None:
            if (time() - start) > 5.0:
                return False
        self.send = msg
        return True
    
if __name__ == '__main__':
    test = I2c()
    while True:
        pass
        #test.write_value(1)
