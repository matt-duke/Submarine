import common
import control
import setup
from server import Server


setup.run()

control.InternalMonitor.start()

server = Server()
server.start()
