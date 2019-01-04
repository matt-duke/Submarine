import common
from setup.config_parser import config_parser

def run():
    ## By the end of this function, all startup items should be done.
    ## Includes initializing sensors, parsing config file(s), network details, tests, etc.
    common.mode = common.OpMode.startup
    common.config = config_parser('setup/config.ini')
    init_internal_sensors()
    
def init_internal_sensors():
    for n in ['used_ram','ps_ram','free_ram','used_disk','media_disk','tile_disk','cpu_percent','other_disk']:
        common.sensors[n] = common.Sensor(type=0)
    for n in ['total_ram','total_disk']:
        common.sensors[n] = common.Sensor(type=0, check_valid=False)
        
def start_network():
    pass