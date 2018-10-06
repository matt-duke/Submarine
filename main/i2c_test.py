import RPi.GPIO as gpio
import smbus
import time
import sys
bus = smbus.SMBus(1)
address = 0x04

def main():
    while 1:
        bus.write_byte(address, 0x09) # trigger send data
        r = bus.read_i2c_block_data(address, 0)
        print(r[2])
        time.sleep(1)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        #gpio.cleanup()
        sys.exit(0)