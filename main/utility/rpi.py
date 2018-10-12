import logging
logger = logging.getLogger(__name__)
from subprocess import call
import src.config as config

sim = False
try:
    import Rpi.GPIO as GPIO
except:
    sim = True

def gpio_init():
    return

def update():
    logger.debug('update(): started')
    call(['sudo apt-get update'])
    call(['sudo apt-get upgrade'])
    call(['git pull'])
    
def reboot():
    logger.debug('reboot()')
    call(['sudo reboot'])