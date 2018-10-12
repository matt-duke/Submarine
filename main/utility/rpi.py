import logging
logger = logging.getLogger(__name__)
from subprocess import call

sim = False
try:
    import Rpi.GPIO as GPIO
except:
    sim = True

def gpio_init():
    if sim:
        return

def update():
    logger.debug("update(): started")
    if sim:
        return
    logger.debug("update(): started")
    call(["sudo apt-get update"])
    call(["sudo apt-get upgrade"])