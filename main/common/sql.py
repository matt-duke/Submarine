import sqlite3
import logging
import time as t
import os
from shutil import copyfile

import common.config as config
import logging
logger = logging.getLogger(__name__)

## TODO: load table basics on init, add functionality
    
class Database:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.isfile(file_path):
            try:
                conn = sqlite3.connect(file_path)
                conn.close()
            except:
                #log error, remove print
                print('Error')
                return False
                
        self.archive_dir = "db/archive/"
        try:
            os.mkdir(self.archive_dir)
        except:
            pass
        
    def show_tables(self):
        sql_cmd = "select name from sqlite_master where type = 'table';"
        return self.run_command(sql_cmd)
    
    def create_table(self, table_name, columns):
        if os.path.isfile_path(self.file_path):
            if config.debug[0]:
                os.remove(self.file_path)
            else:
                backup_file_path = self.archive_dir + (self.file_path.split('/')[-1])[:-3] + '_' + str(int(t.time())) + '.db'
                copyfile(self.file_path, backup_file_path)
                os.remove(self.file_path)

        sql_cmd = 'CREATE TABLE {} (\n'.format(table_name)
        for k, v in columns.items():
            sql_cmd += '\t{} {}, \n'.format(k, v)
        sql_cmd = sql_cmd[:-3] + '\n);'
        logger.debug("create_table(): {} in {}".format(self.table_name, self.file_path))
        try:
            c.execute(sql_cmd)
        except Exception as e:
            logger.error('create_table(): Error: '+str(e))
        conn.commit()
        conn.close()
        
    def add_row(self, data, table=""):
        conn = sqlite3.connect(self.file_path)
        c = conn.cursor()
        time = get_time()
        sql_cmd = "INSERT INTO " + self.table_name + " VALUES ("
        for k, v in columns.items():
            add = "NameError"
            try:
                add = data[k]
            except:
                pass
            if k is 'time':
                add = "'{}'".format(time[0])
            elif k is 'date':
                add = "'{}'".format(time[1])
            elif k is 'mode':
                add = "'{}'".format(config.modeList[config.mode])
            sql_cmd += "{}, ".format(add)
        sql_cmd = sql_cmd[:-2] + ');'
        run_command(sql_cmd)
    
    
    def last_row(self, table=""):
        #select first table by default
        if table == "":
            table = self.show_tables()[0]
        sql_cmd = "SELECT * FROM {} ORDER BY rowid DESC LIMIT 1;".format(table)
        return self.run_command(sql_cmd)
        
    def run_command(self, sql_cmd):
        conn = sqlite3.connect(self.file_path)
        c = conn.cursor()
        c.execute(sql_cmd)
        data = c.fetchall()[0]
        if 'INSERT' in sql_cmd.upper():
            conn.commit()
        conn.close()
        return data