#!/home/pi/Submarine-v2/setup/venv/bin/python3
import sys

sys.path.insert(0,"/home/pi/Submarine-v2/server")

from index import app as application
application.secret_key = 'anything you wish'
