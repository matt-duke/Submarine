from multiprocessing import Pipe
import core

class ModuleServer(core.BaseClass):
    def __init__(self):
        self.server_conn, client_conn = Pipe()
        
        core.BaseClass.__init__(self)
        
    def start(self):
    
        def __run(self, ThreadSelf):