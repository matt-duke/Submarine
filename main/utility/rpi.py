from subprocess import call
import common

import logging
logger = logging.getLogger(__name__)

sim = False
try:
    import Rpi.GPIO as GPIO
except:
    sim = True

def gpio_init():
    return

def toggle_wifi():
    if sp_run('ifconfig | grep -c wlan', shell=True):
        sp_run('rfkill block wifi', shell=True)
    else:
        sp_run('rfkill unblock wifi', shell=True)

def update():
    logger.debug('update(): started')
    call(['sudo apt-get update'])
    call(['sudo apt-get upgrade'])
    call(['git pull'])
    
def reboot():
    logger.debug('reboot()')
    call(['sudo reboot'])