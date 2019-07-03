import common
import core
import os
import queue
from time import time, sleep

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
        self.SerialThread = self.threads.add('SerialThread', self.__comm)
    
    @staticmethod
    def __comm(self, threadSelf):
        if not self.serial.is_open:
            raise Exception('Serial closed. Exiting.')
        if self.serial.in_waiting > 0:
            self.lock.acquire()
            buffer = self.serial.readline()
            self.lock.release()
            if buffer != b'':
                self.logger.debug(buffer)
    
    def __serial_wait_cond(self): return self.serial.in_waiting > 0
    
    def write(self, msg):
        with self.lock:
            #if type(msg)==bytes:
            self.logger.debug('Writing message: {}'.format(repr(msg)))
            self.serial.write(msg)
            self.wait(self.__serial_wait_cond)
            buffer = self.serial.readline()
            filtered_buffer = bytes(buffer[0:-2])
            self.logger.debug('Received msg: {} ({})'.format(repr(buffer), filtered_buffer))
            return filtered_buffer
            #else:
             #   self.logger.error('Invalid message {}'.format(msg))
    
    def _open_serial(self, baudrate=115200, timeout=0, write_timeout=0):
        self.lock.acquire()
        if self.serial.is_open:
            #self.logger.debug('Serial already open')
            pass
        else:
            try:
                self.serial.port = self.port
                self.serial.baudrate = baudrate
                self.serial.timeout = timeout
                self.serial.write_timeout = write_timeout
                self.serial.open()
            except:
                self.logger.critical('MCU not detected on {}'.format(self.port))       
        sleep(0.5)
        self.lock.release()
    
    def _close_serial(self):
        self.lock.acquire()
        self.serial.close()
        self.lock.release()

    def __upload(self, hexFile):
        self._close_serial()
        if self.fileExists(hexFile):
            self.logger.debug('Flashing atmega2560...')
            cmd = r'/usr/share/arduino/hardware/tools/avr/../avrdude -q -V -p atmega2560 -C /usr/share/arduino/hardware/tools/avr/../avrdude.conf -D -c wiring -b 115200 -P {0} -U flash:w:{1}:i'.format(self.port, hexFile)
            if not self.systemCall(cmd):
                raise Exception('ArduinoError')
    
    def reset(self):
        self._close_serial()
        self._open_serial()
        
    def connect(self):
        if self.SerialThread.is_alive():
            self.logger.info('Already connected')
            return
        self.logger.info('Connecting to MCU...')
        self._open_serial()
        with self.lock:
            if not self.wait(self.__serial_wait_cond, timeout=10):
                logger.error('MCU failed to connect')
            self.serial.reset_input_buffer()
            
        self.SerialThread.start(loop=True, sleep=2)
        self.logger.info('Connected')
        
    def disconnect(self):
        self.logger.info('Disconnecting from MCU...')
        self.SerialThread.kill(block=True)
        self._close_serial
        self.logger.info('Disconnected')
        