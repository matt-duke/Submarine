from src.comm import *

def var_init():
    global modeList, mode, sensor, debug, sim
    sensor = []
    debug = True
    sim = True
    
    names = ["Ax", "Ay", "Az"]
    for n in names:
        s = Sensor()
        s.name = n
        sensor.append(s)
    modeList = ["init", "normal", "emergency"]
    mode = 0