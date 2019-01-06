import common
import logging
from pathlib import Path 

logger = logging.getLogger(__name__)

def start():
    logger.info('Setting up interfaces')
    i = 0
    while common.config.has_section('BUS_'+str(i)):
        bus_name = 'BUS_'+str(i)
        data = {'Path': common.config.get(bus_name, 'Path').replace('/','.').replace('.py',''),
                'Enabled': common.config.getboolean(bus_name, 'Enabled'),
                'LogLevel': common.log_dict[common.config.get(bus_name, 'LogLevel')],
                'RefreshRate': common.config.get(bus_name, 'RefreshRate')}
        common.bus.append(common.Bus(bus_name, data))
        common.bus[i].logger.info('Adding data bus: '+bus_name)
        i=i+1

    for option in common.config.options('SENSOR'):
        data = common.config.get('SENSOR', option)
        if option == 'validitytimeout':
            common.Sensor.validity_timeout = int(data)
            continue
        data = data.split(',')
        try:
            bus_index = int(data[0])
            common.bus[bus_index].add_sensor(name=option,type=int(data[1]),check_valid=bool(data[2]))
                                                             
            common.bus[bus_index].logger.info('Adding sensor: {} to bus BUS_{}'.format(option, bus_index))
        except Exception as e:
            common.bus[bus_index].logger.error('Error adding SENSOR: {} - {}'.format(option, e))