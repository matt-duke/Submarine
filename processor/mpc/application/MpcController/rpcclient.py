import xmlrpc.client
import socket
from threading import Thread

HOST = '127.0.0.1'  # The server's hostname or IP address


def remote_fn(stream_output=True):
    with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
        port = proxy.iperf3()['port']
    
    if stream_output:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, port))
            except:
                print('Failure connecting to stream')
            while True:
                try:
                    data = s.recv(1024)
                    if len(data) > 0:
                        print(data)
                except:
                    break
            
remote_fn()