from xmlrpc.server import SimpleXMLRPCServer
import serialtcp

import subprocess
from threading import Thread, Event
from queue import Queue


import socket

INITIAL_PORT = 5000
NUM_OF_PORTS = 100
RPC_PORT = 8000
HOST = '127.0.0.1'

class BackgroundStream(Thread):
    Ports = list(range(INITIAL_PORT, INITIAL_PORT+NUM_OF_PORTS))
    def __init__(self, cmd, host=HOST):
        self.host=host
        self.port = StreamProcess.Ports.pop(0)
        self.closeEvent = Event()
        self.closeEvent.clear()
        self.cmd = cmd
        
        Thread.__init__(self, daemon=False)
    
    
    def start(self):
        self.__setup()
        print('Starting process {}'.format(self.cmd))
        Thread.start(self)
    
    def __setup(self):
        pass
    
    def __read(self):
        return None
        
    def __cleanup(self):
        pass
    
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                while True:
                    try:
                        data = bytearray(self.__read())
                        conn.sendall(data)
                    except:
                        self.closeEvent.set()
                    
                    if self.closeEvent.is_set() or self.proc.poll()!=None:
                        self.__cleanup()
                        s.close()
                        StreamProcess.Ports[0] = self.port
                        print('Ending process {}'.format(self.cmd))
                        return

class StreamProcess(BackgroundStream):
    def __read(self):
        return self.proc.stdout.readline()
    def __setup(self):
        self.proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def __cleanup(self):
        self.proc.kill()

class RPCServer():
    def __init__(self):
        server  = SimpleXMLRPCServer(("localhost", RPC_PORT))
        print("Listening on port 8000...")
        server.register_function(self.iperf3, "iperf3")
        server.register_function(self.start_serial_server, "start_serial_server")
        
        print(dir(serialtcp))
        server.serve_forever()

    def start_serial_server(self):
        serialtcp()
        

    def iperf3(config={}):
        key_map = {'--client', '-c',
                   '--port', '-p',
                   '--time', '-t',
                   '--bind', '-b'
                   }
        
        for key, item in config.items():  
            try:
                config[key_map[key]] = config.pop(key)
            except Exception as e:
                print(e)
            
        default_config = {'-c': '',
                          '-p': '5000',
                          '-t': '100',
                          '-B': '172.30.3.11',
        
        }
        config = {**default_config, **config}
        cmd = ['iperf3'] + list(sum(config.items(), ()))
        #cmd = ['ping', '8.8.8.8', '-t']
        sp = StreamProcess(cmd)
        sp.start()
        return {'port': sp.port, 'success': True}
        
if __name__ == '__main__':
    RPCServer()