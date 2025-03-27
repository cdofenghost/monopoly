import socket
import sys

class Client:
    def __init__(self, host, port):
        self.PORT = port
        self.HOST = host

    def connect(self):
        with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))

            s.sendall(b'Hello World')
            data = s.recv(1024)

        print(f"Received {data}")