import sqlite3
import logging
import time as t
import os
from shutil import copyfile

import src.config as config

logger = logging.getLogger(__name__)

## TODO: archive old db if debug is off, mitigate "table already exists error"

def get_time():
    tm =  t.localtime(t.time())
    date = tm.tm_year+'-'+tm.tm_mon+'-'+tm.tm_mday
    time = tm.tm_hour+':'+tm.tm_min+':'+tm.tm_sec
    return time, date
 
class Table():
    def __init__(self, file, table_name, columns):
        self.file = file
        #self.file_path = file.replace(file.split('/')[-1], '')
        self.table_name = table_name
        self.columns = columns
        self.archive_dir = "db/archive/"
        
    def create_table(self):
        if os.path.isfile(self.file):
            if config.debug:
                os.remove(self.file)
            else:
                backup_file = self.archive_dir + self.file.split('/')[-1] + str(int(t.time())) + '.db'
                copyfile(self.file, backup_file)
                os.remove(self.file)
        conn = sqlite3.connect(self.file)
        c = conn.cursor()
        sql_cmd = 'CREATE TABLE {} (\n'.format(self.table_name)
        for k, v in self.columns.items():
            sql_cmd += '\t{} {}, \n'.format(k, v)
        sql_cmd = sql_cmd[:(len(sql_cmd)-3)] + '\n);'
        logger.debug("create_table(): {} in {}".format(self.table_name, self.file))
        try:
            c.execute(sql_cmd)
        except:
            pass
        conn.commit()
        conn.close()
        
    def add_row(self, table=""):
        conn = sqlite3.connect(self.file)
        c = conn.cursor()
        time = get_time()
        sql_cmd = "INSERT INTO " + self.table_name + " VALUES ("
        for k, v in self.columns.items():
            add = k
            if k is 'time':
                add = "'{}'".format(time[0])
            elif k is 'date':
                add = "'{}'".format(time[1])
            sql_cmd += "{}, ".format(add)
        c.execute(sql_cmd)
        conn.commit()
        conn.close()
        