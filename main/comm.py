
try:
	import smbus
except:
	sim = True
	
bus = smbus.SMBus(1)
adr = 0x04

class Sensor:
    def __init__(self):
        self.value = None
		self.type = None
        self.name = None

	def read_value(val=0x09):
		bus.write_byte(adr, val) # trigger send data
        r = bus.read_i2c_block_data(adr, 0)
        self.value = r[2]
		return self.value
    
	def write_value():
		bus.write_byte(adr, msg)