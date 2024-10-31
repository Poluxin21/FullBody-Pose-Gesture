import socket

class SocketAdapter:
    def __init__(self, ip="127.0.0.1", port=5052):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (ip, port)

    def send(self, data):
        self.sock.sendto(data.encode(), self.server_addr)
