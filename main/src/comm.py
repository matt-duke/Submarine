import logging
logger = logging.getLogger(__name__)
import src.config as config
import time as t

try:
    import smbus
    bus = smbus.SMBus(1)
except:
    sim = True


class I2c():
    def __init__(self):
        self.send = None
        
    def connect(self):
        val = 0x09
        adr = 0x04
        while True:
            if not sim:
                bus.write_byte(adr, val) # trigger send data
                r = bus.read_i2c_block_data(adr, 0)
                config.sensor[0].value = r[2]
                t.sleep(1)
                #send self.send
                #self.send = None
            else:
                config.sensor[0].value = -1
                data = {"sensor_id": 0, "value": config.sensor[0].value}
                config.data_db.add_row(data)
                t.sleep(3)
                config.sensor[0].value = 1
                data = {"sensor_id": 0, "value": config.sensor[0].value}
                config.data_db.add_row(data)
                t.sleep(3)

    def write_value(self, msg):
        start = t.time()
        while self.send != None:
            if (t.time - start) > 5.0:
                return False
        self.send = msg
        return True
