import logging
logger = logging.getLogger(__name__)

try:
    import smbus
    bus = smbus.SMBus(1)
except:
    sim = True
    
adr = 0x04

class Sensor:
    def __init__(self):
        self.value = None
        self.type = None
        self.name = None

    def read_value(val=0x09):
        if not sim:
            bus.write_byte(adr, val) # trigger send data
            r = bus.read_i2c_block_data(adr, 0)
            self.value = r[2]
        else:
            self.value = -1
        return self.value
    
    def write_value():
        if not sim:
            bus.write_byte(adr, msg)
        else:
            return