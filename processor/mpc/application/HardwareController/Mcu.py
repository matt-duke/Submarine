import common
import core
import os

from enum import Enum
import struct

'''
Class used to communicate with Arduino Mega (Atmel 2560)
Includes the ability to update and flash the chip from serial USB

LINKS:
https://github.com/araffin/arduino-robust-serial
'''

class serial:
    class Serial(core.BaseClass):
        def __init__(self, port, baudrate, timeout, writeTimeout):
            core.BaseClass.__init__(self)
            self.logger.info('Starting simulated serial object')
            
        def close(self):
            self.logger.info('Closing serial simulator')

class McuClass(core.BaseClass):
    def __init__(self):
        core.BaseClass.__init__(self)
        self.test = common.CDS.get('testmode')
        self.serial = None
    
    def open_serial(self, port, baudrate=115200, timeout=0, write_timeout=0):
        if not self.test:
            import serial
        self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout, writeTimeout=write_timeout)
        
    def close_serial(self):
        if self.serial != None:
            self.serial.close()
            self.serial = None

    def upload(self, hexFile):
        if self.fileExists(hexFile):
            if self.systemCall(['']):
                return True
        return False
        


class MsgClass(Enum):
    HELLO = 0
    SERVO = 1
    MOTOR = 2
    ALREADY_CONNECTED = 3
    ERROR = 4
    RECEIVED = 5
    STOP = 6

    def read_order(f):
        """
        :param f: file handler or serial file
        :return: (Order Enum Object)
        """
        return Order(read_i8(f))

    def read_i8(f):
        """
        :param f: file handler or serial file
        :return: (int8_t)
        """
        return struct.unpack('<b', bytearray(f.read(1)))[0]


    def read_i16(f):
        """
        :param f: file handler or serial file
        :return: (int16_t)
        """
        return struct.unpack('<h', bytearray(f.read(2)))[0]


    def read_i32(f):
        """
        :param f: file handler or serial file
        :return: (int32_t)
        """
        return struct.unpack('<l', bytearray(f.read(4)))[0]


    def write_i8(f, value):
        """
        :param f: file handler or serial file
        :param value: (int8_t)
        """
        if -128 <= value <= 127:
            f.write(struct.pack('<b', value))
        else:
            print("Value error:{}".format(value))


    def write_order(f, order):
        """
        :param f: file handler or serial file
        :param order: (Order Enum Object)
        """
        write_i8(f, order.value)


    def write_i16(f, value):
        """
        :param f: file handler or serial file
        :param value: (int16_t)
        """
        f.write(struct.pack('<h', value))


    def write_i32(f, value):
        """
        :param f: file handler or serial file
        :param value: (int32_t)
        """
        f.write(struct.pack('<l', value))


    def decode_order(f, byte, debug=False):
        """
        :param f: file handler or serial file
        :param byte: (int8_t)
        :param debug: (bool) whether to print or not received messages
        """
        try:
            order = Order(byte)
            if order == Order.HELLO:
                msg = "HELLO"
            elif order == Order.SERVO:
                angle = read_i16(f)
                # Bit representation
                # print('{0:016b}'.format(angle))
                msg = "SERVO {}".format(angle)
            elif order == Order.MOTOR:
                speed = read_i8(f)
                msg = "motor {}".format(speed)
            elif order == Order.ALREADY_CONNECTED:
                msg = "ALREADY_CONNECTED"
            elif order == Order.ERROR:
                error_code = read_i16(f)
                msg = "Error {}".format(error_code)
            elif order == Order.RECEIVED:
                msg = "RECEIVED"
            elif order == Order.STOP:
                msg = "STOP"
            else:
                msg = ""
                print("Unknown Order", byte)

            if debug:
                print(msg)
        except Exception as e:
            print("Error decoding order {}: {}".format(byte, e))
            print('byte={0:08b}'.format(byte))