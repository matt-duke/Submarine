import common
import core
import socket

#https://wiki.python.org/moin/TcpCommunication

class SocketClient(common.BaseClass):
    def __init__(self):
        common.BaseClass.__init__(self)
        self.IP = '127.0.0.1'
        self.PORT = 5000
        self.BUFFER_SIZE = 1024
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        self.s.connect((self.IP,self.PORT))
        
    def send(self, msg):
        self.s.send(msg)
        data = s.recv(BUFFER_SIZE)
        
class SocketServer(common.BaseClass):
    def __init__(self):
        common.BaseClass.__init__(self)
        self.IP = '127.0.0.1'
        self.PORT = 5000
        self.BUFFER_SIZE = 20
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def start(self):
        self.s.bind((self.IP,self.PORT))
        self.s.listen(1)
        conn, addr = s.accept()
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
                print("received data: {}".format(data)
                conn.send(data)  # echo
        conn.close()
        
    def send(self, msg):
        self.s.send(msg)
        data = s.recv(BUFFER_SIZE)