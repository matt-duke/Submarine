import core

from . import DataTypes

import logging

import sqlite3
from datetime import datetime
import os


class CvtManager():    
    def __init__(self):    
        self.cvt_server = core.ProxyServer()
        self.cvt_server.register('Sensor', DataTypes.SensorClass)
        self.cvt_server.register('Data', DataTypes.DataClass)
        self.cvt_server.start()
        self.logger.info('CVT server started')
        self.cvt = self.cvt_server.Namespace()
        self.cvt.wifi = self.cvt_server.Namespace()
        self.cvt.gui = self.cvt_server.Namespace()
        
        self.cvt.platform = self.cvt_server.Data(str)
        self.cvt.testmode = self.cvt_server.Data(bool)
        self.cvt.opmode = self.cvt_server.Data(int)
        self.cvt.resolution_width = self.cvt_server.Data(int)
        self.cvt.resolution_height = self.cvt_server.Data(int)
        self.cvt.framerate = self.cvt_server.Data(int)
        self.cvt.wifi.ssid = self.cvt_server.Data(str)
        self.cvt.wifi.key = self.cvt_server.Data(str)
        self.cvt.gui.enabled = self.cvt_server.Data(bool)
        self.cvt.gui.refresh = self.cvt_server.Data(int)
        
        self.cvt.batt_voltage = self.cvt_server.Sensor(float, 'V')
        self.cvt.latitude = self.cvt_server.Sensor(float)
        self.cvt.longitude = self.cvt_server.Sensor(float)
        self.cvt.surface_temperature = self.cvt_server.Sensor(float, '\u00b0C')
        self.cvt.water_temperature = self.cvt_server.Sensor(float, '\u00b0C')
        self.cvt.air_temperature = self.cvt_server.Sensor(float, '\u00b0C')
        self.cvt.current = self.cvt_server.Sensor(float, 'A')
        self.cvt.m1_current = self.cvt_server.Sensor(float, 'A')
        self.cvt.m2_current = self.cvt_server.Sensor(float, 'A')
        self.cvt.pressure = self.cvt_server.Sensor(float, 'kPa')
    
    
    def start_logging(self, debug_file):
        pass
        #self.log_thread = Thread(target=self.log_thread_fn, args=(debug_file,))
        #self.log_thread.start()
    
    '''def log_thread_fn(self, debug_file):
        type_map = {int:'INTEGER', float:'REAL', str:'TEXT', bool:'INTEGER'}
        
        sql_table = 'CREATE TABLE data (date TEXT,time TEXT,'
        for key, item in self.sensors.items():
            sql_table += '{} {},'.format(key, type_map[item.type])
        sql_table = sql_table[:-1]+')'
        conn = sqlite3.connect(debug_file)
        c = conn.cursor()
        c.execute(sql_table)
        c.close()

        insert_into = '('
        for i in range(len(self.sensors)+2):      
            insert_into += '?,'
        insert_into = insert_into[:-1]+')'
        
        while True:
            logger.debug('Writing to sql database')
            lastrowid = 0
            data = [item.read() for key, item in self.sensors.items()]
            now = datetime.now()
            datetime_now = [now.strftime('%m/%d/%Y'), now.strftime('%H:%M:%S')]
            
            data = tuple(datetime_now + data)
            
            c = conn.cursor()
            c.execute('INSERT INTO data VALUES {};'.format(insert_into), data)
            lastrowid = c.lastrowid
            conn.commit()
            c.close()
            time.sleep(2)
            '''
        