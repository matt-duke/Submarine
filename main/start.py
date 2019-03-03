import common
from src import bus_mgr
from control import monitor
import setup
from server import Server

print('ROV Submarine')
print('v.0.1\n')
setup.run()
bus_mgr.start()

monitor.start()

server = Server()
server.start()
