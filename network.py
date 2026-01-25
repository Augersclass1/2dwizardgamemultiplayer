import socket
import json
import pickle
import struct

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
            self.client.settimeout(5)  # 5 second timeout
            self.player_id = self._receive_message()
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def send(self, data):
        """Send data to server with length prefix"""
        try:
            serialized = pickle.dumps(data)
            # Send length prefix (4 bytes) followed by data
            self.client.sendall(struct.pack("I", len(serialized)) + serialized)
        except socket.error as e:
            print(f"Send error: {e}")
            return False
        return True

    def _receive_message(self, suppress_timeout=False):
        """Receive one complete length-prefixed pickled message"""
        try:
            # First, receive the 4-byte length prefix
            length_data = b""
            while len(length_data) < 4:
                chunk = self.client.recv(4 - len(length_data))
                if not chunk:
                    return None
                length_data += chunk
            
            message_length = struct.unpack("I", length_data)[0]
            
            # Now receive the exact number of bytes needed
            message_data = b""
            while len(message_data) < message_length:
                chunk = self.client.recv(message_length - len(message_data))
                if not chunk:
                    return None
                message_data += chunk
            
            # Unpickle and return
            obj = pickle.loads(message_data)
            return obj
        except socket.timeout:
            # Suppress timeout messages during normal gameplay (non-blocking mode)
            if not suppress_timeout:
                print("Socket timeout while receiving")
            return None
        except Exception as e:
            print(f"Message receive error: {e}")
            return None

    def receive(self):
        """Receive data from server (non-blocking with timeout)"""
        try:
            self.client.settimeout(0.1)
            # Suppress timeout messages during non-blocking receives
            return self._receive_message(suppress_timeout=True)
        except socket.timeout:
            return None
        except Exception as e:
            print(f"Receive error: {e}")
            return None

    def receive_blocking(self):
        """Receive data from server (blocking)"""
        try:
            self.client.settimeout(None)
            # Don't suppress for blocking receives - timeouts are unexpected
            return self._receive_message(suppress_timeout=False)
        except Exception as e:
            print(f"Receive error: {e}")
            return None

    def set_blocking_mode(self):
        """Set socket to blocking mode"""
        self.client.settimeout(None)

    def set_non_blocking_mode(self):
        """Set socket to non-blocking with timeout"""
        self.client.settimeout(0.1)

    def disconnect(self):
        """Disconnect from server"""
        try:
            self.client.close()
        except:
            pass
