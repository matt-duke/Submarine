from subprocess import run
import common

import logging
logger = logging.getLogger(__name__)

try:
    import Rpi.GPIO as GPIO

def gpio_init():
    return

def toggle_wifi():
    if common.PLATFORM = 'Linux'
        if run('ifconfig | grep -c wlan'):
            run('rfkill block wifi')
        else:
            run('rfkill unblock wifi')
    else:
        logger.error('Platform not supported')
        
def update():
    if common.PLATFORM = 'Linux'
        logger.debug('update(): started')
        run('sudo apt-get update')
        run('sudo apt-get upgrade')
        run('git pull')
    else:
        logger.error('Platform not supported')
    
def reboot():
    if common.PLATFORM = 'Linux'
        logger.debug('Reboot initialized')
        run('sudo reboot')
    else:
        logger.error('Platform not supported')