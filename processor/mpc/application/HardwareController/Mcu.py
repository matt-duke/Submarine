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
http://www.raspberryvi.org/stories/arduino-cli.html
https://www.avrfreaks.net/forum/avrdude-reset-command
'''

class serial:
    class Serial(core.BaseClass):
        def __init__(self, port, baudrate, timeout, writeTimeout):
            core.BaseClass.__init__(self)
            self.logger.info('Starting simulated serial object')
            self.is_open = True
            
        def close(self):
            self.logger.info('Closing serial simulator')
            self.is_open = False

class McuClass(core.BaseClass):
    def __init__(self, port):
        core.BaseClass.__init__(self)
        self.serial = None
        self.port = port
        
        if not common.testmode:
            import serial
            
        self.serial = serial.Serial()
        self.serialReadThread = self.addThread('serialRead', self.serialRead, loop=True, sleep=0.1)
    
    def open_serial(self, baudrate=115200, timeout=0, write_timeout=0):
        try:
            self.serial.port = self.port
            self.serial.baudrate = baudrate
            self.serial.timeout = timeout
            self.serial.write_timeout = write_timeout
            self.serial.open()
            self.serialReadThread.start()
        except:
            self.logger.critical('MCU not detected on {}'.format(self.port))
    
    @staticmethod
    def serialRead(self, threadSelf):
        if self.serial.is_open:
            buffer = self.serial.readline()
            if buffer != b'':
                self.logger.info(buffer)
        
    def close_serial(self):
        self.serialReadThread.lock.acquire()
        if self.serial.is_open:
            self.serial.close()

    def upload(self, hexFile):
        self.close_serial()
        if self.fileExists(hexFile):
            cmd = r'/usr/share/arduino/hardware/tools/avr/../avrdude -q -V -p atmega2560 -C /usr/share/arduino/hardware/tools/avr/../avrdude.conf -D -c wiring -b 115200 -P {0} -U flash:w:{1}:i'.format(self.port, hexFile)
            if not self.systemCall(cmd.split(' ')):
                raise Exception('ArduinoError')
    
    def reset(self):
        self.close_serial()
        self.open_serial()

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