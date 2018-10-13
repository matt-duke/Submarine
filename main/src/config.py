import logging

def init():
    global debug, modeList, mode, sensor
    
    data_db = None
    debug = [True, True] #[debug mode, sim mode]
    if debug:
        logging.basicConfig(filename = 'debug.log', filemode ='w', level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    sensor = []
    names = ["Ax", "Ay", "Az"]
    for n in names:
        s = Sensor()
        s.name = n
        sensor.append(s)
    modeList = ["test", "init", "normal", "emergency"]
    mode = 0

def init_db():
    import src.sql as sql
    global data_db
    db_file_name = "db/test.db"
    db_table_name = "test"
    db_columns = {
        "date": "char(10)",
        "time": "char(8)", 
        "mode": "varchar(255)", 
        "sensor_id": "varchar(255)", 
        "value": "varchar(255)"
    }
    data_db = sql.Table(db_file_name, db_table_name, db_columns)
    data_db.create_table()
    
class Sensor:
    def __init__(self):
        self.value = None
        self.type = None
        self.name = None