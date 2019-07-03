import core

import time

import sqlite3
from datetime import datetime
import os


class SensorClass():
    timeout = 30
    def __init__(self, type):
        self.value = None
        self.type = type
        self.valid = False
        self.timestamp = 0
        
    def set(self, val):
        self.value = self.type(val)
        self.timestamp = time.time()
        self.valid = True
        
    def get(self):           
        if all([((time.time()-self.timestamp) > SensorClass.timeout)]):
            self.valid = False
        return self.value
        
    def is_valid(self):
        return self.valid


class CvtManager(core.BaseClass):    
    def __init__(self):
        core.BaseClass.__init__(self)
    
        self.cvt_server = core.ProxyServer()
        self.cvt_server.register('Sensor', SensorClass)
        self.cvt_server.start()
        self.logger.info('CVT server started')
        self.cvt = self.cvt_server.Namespace()
        
        self.cvt.batt_voltage = self.cvt_server.Sensor(int)
        
        self.cvt.platform = ''
        self.cvt.testmode = False
        self.cvt.opmode = 'initial'
    
    
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
        