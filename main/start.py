import common
from src import bus_mgr
import setup
import server

print('ROV Submarine')
print('v.0.0.1\n')
setup.run()
bus_mgr.start()
server.start()
