import src.sql as sql
import logging

def var_init():
    if True:
        logging.basicConfig(filename = 'debug.log', filemode ='w', level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    global modeList, mode, sensor, data_db
    
    db_file_name = "db/test.db"
    db_table_name = "test"
    db_columns = {
        "time": "varchar(255)", 
        "status": "varchar(255)", 
        "sensor_id": "varchar(255)", 
        "value": "varchar(255)"
    }
    data_db = sql.Table(db_file_name, db_table_name, db_columns)
    data_db.create_table()
    
    sensor = []
    names = ["Ax", "Ay", "Az"]
    for n in names:
        s = Sensor()
        s.name = n
        sensor.append(s)
    modeList = ["init", "normal", "emergency"]
    mode = 0
    
class Sensor:
    def __init__(self):
        self.value = None
        self.type = None
        self.name = None