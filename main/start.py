import common
from src import bus_mgr
import setup
from server import Server

print('ROV Submarine')
print('v.0.1\n')
setup.run()
bus_mgr.start()

server = Server()
server.start()
