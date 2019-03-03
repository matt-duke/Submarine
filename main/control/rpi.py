from subprocess import run
import common

import logging
logger = logging.getLogger(__name__)

if common.PLATFORM == 'Linux':
    import Rpi.GPIO as GPIO

#RPM
FAN_STEP = 10
FAN_MAX = 200
    
def gpio_init():
    return

def set_fan(percent):
    fan_speed_sensor = common.get_sensor('fan_speed')
    #print(round((percent*(FAN_MAX))/FAN_STEP)*FAN_STEP == fan_speed_sensor.read())
    return
    if round((percent*(FAN_MAX))/FAN_STEP)*FAN_STEP == fan_speed_sensor.read():
        logger.debug('Setting fan speed to {}%'.format(percent*100))
    if common.PLATFORM == 'Linux':
        pass
    else:
        pass
        #logger.error('Platform not supported')

def toggle_wifi():
    if common.PLATFORM == 'Linux':
        if run('ifconfig | grep -c wlan'):
            run('rfkill block wifi')
        else:
            run('rfkill unblock wifi')
    else:
        logger.error('Platform not supported')
        
def update():
    if common.PLATFORM == 'Linux':
        logger.debug('update(): started')
        run('sudo apt-get update')
        run('sudo apt-get upgrade')
        run('git pull')
    else:
        logger.error('Platform not supported')
    
def reboot():
    if common.PLATFORM == 'Linux':
        logger.debug('Reboot initialized')
        run('sudo reboot')
    else:
        logger.error('Platform not supported')