import logging
logger = logging.getLogger(__name__)

import time

from threading import Thread
import sqlite3
from datetime import datetime
import os

class Sensor:
    timeout = 30
    def __init__(self, name, type):
        self.value = None
        self.type = type
        self.name = name
        self.valid = False
        self.timestamp = 0
        
    def write(self, val):
        self.value = self.type(val)
        self.timestamp = time.time()
        self.valid = True
        
    def read(self):           
        if all([((time.time()-self.timestamp) > Sensor.timeout)]):
            self.valid = False
        return self.value

class Value:
    def __init__(self, name, type):
        self.value = None
        self.type = type
        self.name = name
        
    def write(self, val):
        self.value = self.type(val)
    
    def read(self):
        return self.value

        
class CommonDataStructure():    
    def __init__(self):
        self.sensors = {}
        self.values = {}
        
        self.add_sensor('batt_voltage', int)
        self.add_sensor('internal_voltage', int)
        self.add_sensor('external_press', int)
        self.add_sensor('depth', int)
        self.add_sensor('m1_current', int)
        self.add_sensor('m2_current', int)
        self.add_sensor('free_ram', int)
        self.add_sensor('ps_ram', int)
        self.add_sensor('cpu_use', int)
        self.add_sensor('cpu_temp', float)
        
        self.add_value('total_ram', int)
        self.add_value('total_disk', int)
        self.add_value('used_disk', int)
        self.add_value('media_disk', int)
        self.add_value('tile_disk', int)
        self.add_value('fan_speed', int)
        self.add_value('platform', str)
        self.add_value('testmode', bool)
        
        self.size = len(self.sensors)+len(self.values)
    
    def start_logging(self, debug_file):
        self.log_thread = Thread(target=self.log_thread_fn, args=(debug_file,))
        self.log_thread.start()
    
    def log_thread_fn(self, debug_file):
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
        
    def add_sensor(self, name, type):
        self.sensors[name] = Sensor(name, type)
    
    def add_value(self, name, type):
        self.values[name] = Value(name, type)
    
    def get(self, key):
        if key in self.sensors.keys():
            return self.sensors[key]
        elif key in self.values.keys():
            return self.values[key]
        else:
            logger.critical("Sensor "+key+" doesn't exist")
    
    def write(self, key, value):
        self.get(key).write(value)
        
    def read(self, key):
        return self.get(key).read()
        