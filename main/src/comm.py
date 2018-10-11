import logging
logger = logging.getLogger(__name__)
import src.config as config
from time import sleep

try:
    import smbus
    bus = smbus.SMBus(1)
except:
    sim = True
    
adr = 0x04

def start_i2c_read():
    val=0x09
    while True:
        if not sim:
            bus.write_byte(adr, val) # trigger send data
            r = bus.read_i2c_block_data(adr, 0)
            config.sensor[0].value = r[2]
        else:
            config.sensor[0].value = -1
            sleep(3)
            config.sensor[0].value = 1
            sleep(3)
def write_value():
    if not sim:
        bus.write_byte(adr, msg)
    else:
        return