from pythonosc import udp_client

class SocketAdapter:
    def __init__(self, ip="127.0.0.1", port=9001):
        self.client = udp_client.SimpleUDPClient(ip, port)

    def send(self, data):
        for param, value in data.items():
            self.client.send_message(param, value)
            print(f"Sent OSC message: {param} = {value}")
