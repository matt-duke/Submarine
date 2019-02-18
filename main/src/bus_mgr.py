import common
import logging
from pathlib import Path 

logger = logging.getLogger(__name__)

def start():
    logger.info('Setting up interfaces')
    i = 0
    while common.config.has_section('BUS_'+str(i)):
        bus_name = 'BUS_'+str(i)
        data = {'Module': common.config.get(bus_name, 'Module').replace('/','.').replace('.py',''),
                'Enabled': common.config.getboolean(bus_name, 'Enabled'),
                'LogLevel': common.log_dict[common.config.get(bus_name, 'LogLevel')],
                'RefreshRate': common.config.getint(bus_name, 'RefreshRate')}
        common.BUS.append(common.Bus(bus_name, data))
        common.BUS[i].logger.info('Adding data bus: '+bus_name)
        i=i+1
            
    for bus in common.BUS:
        bus.start()