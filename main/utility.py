import time as t
import logger

sim = False
try:
	from picamera import PiCamera
	import Rpi.GPIO as GPIO
	from subprocess import call
except:
	sim = True
	
cam = None

def curr_time(start=1506211200):
    return t.time() - start

def take_photo(path="home/pi/Pictures", res=(800,600)):
	time = curr_time()
	filename = "/{}/image{}.jpg".format(path, time)
	logger.debug("take_photo(): {}".format(filename))
	if sim:
		return
	else:
		if cam is None:
			cam = PiCamera()
		cam.resolution = res
		cam.capture(filename)
		logger.debug("take_photo(): Success")
		cam = None
	
def start_recording(path="home/pi/Videos", res=(800,600)):
	time = curr_time()
	filename = "/{}/video{}.mpg".format(path, time)
	logger.debug("start_recording(): started {}".format(filename))
	if sim:
		return
	else:	
		if cam is None:
			cam = PiCamera()
		else:
			logger.error("start_recording(): Camera already initialized.")
			return False
		cam.resolution = res
		cam.start_recording()
	
def stop_recording():
	logger.debug("stop_recording()")
	if sim:
		return
	else:
		if cam not None:
			cam.stop_recording()
			cam = None

def update():
	logger.debug("update(): started")
	if sim:
		return
	else:
		logger.debug("update(): started")
		call(["sudo apt-get update"])
		call(["sudo apt-get upgrade"])