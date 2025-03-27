import socket
import sys

class Host:
    def __init__(self, host: str, port: int):
        self.HOST = host
        self.PORT = port

    def run(self):
        with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, addr = s.accept()

            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)

                    if not data:
                        break
                    
                    conn.sendall(data)
    
    