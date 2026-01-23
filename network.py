import socket
import json
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = None
        self.addr = None
        self.player_id = None

    def connect(self, host="localhost", port=5555):
        """Connect to the server"""
        try:
            self.server = (host, port)
            self.client.connect(self.server)
            self.player_id = self.receive()
            return True
        except:
            return False

    def send(self, data):
        """Send data to server"""
        try:
            self.client.sendall(pickle.dumps(data))
        except socket.error as e:
            print(f"Send error: {e}")
            return False
        return True

    def receive(self):
        """Receive data from server"""
        try:
            data = b""
            while True:
                chunk = self.client.recv(4096)
                if not chunk:
                    break
                data += chunk
                try:
                    return pickle.loads(data)
                except:
                    continue
        except socket.error as e:
            print(f"Receive error: {e}")
            return None

    def disconnect(self):
        """Disconnect from server"""
        try:
            self.client.close()
        except:
            pass
