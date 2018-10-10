from comm import *

def init():
	global modeList, mode
	global sensor[]
	global debug = True
	global sim = True
	
	names = ["Ax", "Ay", "Az"]
	for n in names:
		s = Sensor()
		s.name = n
		sensor.append(s)
	modeList = ["init", "normal", "emergency"]
	mode = 0