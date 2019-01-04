import common
from src import hw_manager
import setup
from webpage import start as start_server

print('ROV Submarine')
print('v.0.0.1\n')
setup.run()
hw_manager.start()

if common.config.getboolean('SERVER', 'enabled'):
    start_server()
