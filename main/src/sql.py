import sqlite3
import logging
logger = logging.getLogger(__name__)
 
class Table():
    def __init__(self, file_name, table_name, columns):
        self.file_name = file_name
        self.table_name = table_name
        self.columns = columns
        
    def create_table(self):
        conn = sqlite3.connect(self.file_name)
        c = conn.cursor()
        sql_cmd = 'CREATE TABLE {} (\n'.format(self.table_name)
        for k, v in self.columns.items():
            sql_cmd += '\t{} {}, \n'.format(k, v)
        sql_cmd = sql_cmd[:(len(sql_cmd)-3)] + '\n);'
        logger.debug("create_table(): {} in {}".format(self.table_name, self.file_name))
        try:
            c.execute(sql_cmd)
        except:
            pass
        conn.commit()
        conn.close()
        
        ## TODO: archive old db if debug is off, mitigate "table already exists error"