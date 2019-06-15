import common
import core

import zerorpc

class RPCServer(core.BaseClass):
    class server(object):
        def mode(self):
            return common.OpMode
        
    def __init__(self):
        self.server = zerorcp.Server(self.server)
        self.server.bind("tcp://0.0.0.0:5000")
    
    def run(self):
        self.server.run()
        