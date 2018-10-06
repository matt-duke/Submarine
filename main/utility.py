from picamera import PiCamera
import Rpi.GPIO as GPIO
import time as t
from subprocess import call

camera = PiCamera()

def take_photo(res=(800,600)):
    camera.resolution = res
    time = curr_time()
    camera.capture('/home/pi/Pictures/image%s.jpg' % time)

def start_recording(res=(800,600)):
    camera.resolution = res
    time = curr_time()
    camera.start_recording('/home/pi/Videos/video%s.jpg' % time)

def curr_time(start=1506211200):
    return t.time() - start

def update():
    call(["sudo apt-get update"])
    call(["sudo apt-get upgrade"])