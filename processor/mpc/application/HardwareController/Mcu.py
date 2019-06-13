import common
import core
import os
import queue
from time import time

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
        self.port = port
        
        if not common.testmode:
            import serial
            
        self.serial = serial.Serial()
        self.msgQueue = queue.Queue()
        self.SerialThread = self.threads.add('SerialThread', self.__comm)
    
    @staticmethod
    def __comm(self, threadSelf):
        if not self.serial.is_open:
            return
        self.lock.acquire(timeout=5)
        try:
            msg = self.msgQueue.get_nowait()
            self.logger.debug('Writing message "{}"'.format(msg))
            self.serial.write(msg)
        except queue.Empty:
            pass
        buffer = self.serial.readline()
        self.lock.release()
        if buffer != b'':
            self.logger.debug(buffer)
    
    def open_serial(self, baudrate=115200, timeout=0, write_timeout=0):
        self.lock.acquire(timeout=5)
        if self.serial.is_open:
            self.logger.debug('Serial already open')
        else:
            try:
                self.serial.port = self.port
                self.serial.baudrate = baudrate
                self.serial.timeout = timeout
                self.serial.write_timeout = write_timeout
                self.serial.open()
            except:
                self.logger.critical('MCU not detected on {}'.format(self.port))
        self.lock.release()   
    
    def close_serial(self):
        self.lock.acquire(timeout=5)
        self.SerialThread.kill(wait=True)
        self.serial.close()
        self.lock.release()

    def upload(self, hexFile):
        self.close_serial()
        if self.fileExists(hexFile):
            cmd = r'/usr/share/arduino/hardware/tools/avr/../avrdude -q -V -p atmega2560 -C /usr/share/arduino/hardware/tools/avr/../avrdude.conf -D -c wiring -b 115200 -P {0} -U flash:w:{1}:i'.format(self.port, hexFile)
            if not self.systemCall(cmd.split(' ')):
                raise Exception('ArduinoError')
    
    def reset(self):
        self.close_serial()
        self.open_serial()
        
    def connect(self):
        self.logger.debug('Connecting to MCU...')
        self.open_serial()
        self.SerialThread.start(loop=True, sleep=2)
        self.logger.debug('Connected')
    