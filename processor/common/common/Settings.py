import json
import core
import common
import Enum

import os

        

class SettingsManager()
    def __init__(self):
        self.proxy_server = core.ProxyServer(address=, port=)
        self.proxy_server.register('settings', SettingsClass)
        self.settings = self.proxy_server.settings()
        
        if os.environ['APP_MODE']:
            self.proxy_server.start()
        else:
            self.proxy_server.connect()
        
    def verify(obj):
        return True