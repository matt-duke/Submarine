import config as c

def debug(msg):
	try:
		f = open("debug.txt", 'w')
		self.f.write(msg)
	finally:
		f.close()
		
def error(msg):
	if c.debug:
		try:
			f = open("debug.txt", 'w')
			self.f.write(msg)
			raise Exception(msg)
		finally:
			f.close()
	else:
		debug(msg)