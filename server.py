import socket
import threading
import pickle
import random
import math
import argparse

# =====================
# CONSTANTS
# =====================
TILE_SIZE = 40
CHUNK_SIZE = 16

AIR = 0
DIRT_TILE = 1
STONE_TILE = 2
GRASS_TILE = 3
SAND_TILE = 4
WOOD_TILE = 5
LEAF_TILE = 6

# =====================
# WORLD GENERATION
# =====================
world = {}

def get_height(global_x):
    base_height = 8
    hill_height = 2
    hill_width = 10

    return int(
        8 +
        4 * math.sin(global_x / hill_width) +
        2 * math.sin(global_x / hill_height)
    )

def generate_tree(tiles, x, y):
    height = random.randint(3, 5)

    for i in range(height):
        if y - i >= 0:
            tiles[y - i][x] = WOOD_TILE

    leaf_start = y - height
    for lx in range(-2, 3):
        for ly in range(-2, 3):
            if abs(lx) + abs(ly) < 4:
                tx = x + lx
                ty = leaf_start + ly
                if 0 <= tx < CHUNK_SIZE and 0 <= ty < CHUNK_SIZE:
                    if tiles[ty][tx] == AIR:
                        tiles[ty][tx] = LEAF_TILE

def generate_chunk(cx, cy):
    tiles = [[AIR for _ in range(CHUNK_SIZE)] for _ in range(CHUNK_SIZE)]

    for y in range(CHUNK_SIZE):
        for x in range(CHUNK_SIZE):
            global_x = cx * CHUNK_SIZE + x
            global_y = cy * CHUNK_SIZE + y
            ground_height = get_height(global_x)
            if global_y > ground_height:
                if global_y == ground_height + 1 and random.random() < 0.7:
                    tiles[y][x] = GRASS_TILE
                elif global_y > ground_height + 4:
                    tiles[y][x] = STONE_TILE if random.random() > 0.05 else DIRT_TILE
                else:
                   tiles[y][x] = STONE_TILE if random.random() < 0.35 else DIRT_TILE

    for x in range(CHUNK_SIZE):
        global_x = cx * CHUNK_SIZE + x
        ground_y = get_height(global_x)
        local_y = ground_y - cy * CHUNK_SIZE
        if 0 <= local_y < CHUNK_SIZE:
            if random.random() < 0.04:
                generate_tree(tiles, x, local_y)

    return tiles

def get_chunk(cx, cy):
    if (cx, cy) not in world:
        world[(cx, cy)] = generate_chunk(cx, cy)
    return world[(cx, cy)]

# =====================
# SERVER CLASS
# =====================
class GameServer:
    def __init__(self, host="localhost", port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}
        self.player_id_counter = 0
        self.lock = threading.Lock()

    def start(self):
        """Start the server"""
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            print(f"Server started on {self.host}:{self.port}")
            
            while True:
                client, addr = self.server.accept()
                print(f"Connection from {addr}")
                
                with self.lock:
                    player_id = self.player_id_counter
                    self.player_id_counter += 1
                
                client.sendall(pickle.dumps(player_id))
                
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client, addr, player_id)
                )
                client_thread.daemon = True
                client_thread.start()
                
                self.clients[player_id] = {
                    "socket": client,
                    "addr": addr,
                    "x": 100,
                    "y": 100,
                    "vel_x": 0,
                    "vel_y": 0,
                    "on_ground": False
                }
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.server.close()

    def handle_client(self, client, addr, player_id):
        """Handle individual client connection"""
        try:
            while True:
                data = self.receive_from_client(client)
                
                if data is None:
                    break
                
                msg_type = data.get("type")
                
                if msg_type == "player_update":
                    # Update player position
                    with self.lock:
                        if player_id in self.clients:
                            self.clients[player_id]["x"] = data["x"]
                            self.clients[player_id]["y"] = data["y"]
                            self.clients[player_id]["vel_x"] = data["vel_x"]
                            self.clients[player_id]["vel_y"] = data["vel_y"]
                            self.clients[player_id]["on_ground"] = data["on_ground"]
                    
                    # Broadcast all players to all clients
                    self.broadcast_players()
                
                elif msg_type == "place_block":
                    # Update world
                    tx, ty = data["x"], data["y"]
                    block_type = data["block_type"]
                    self.place_block(tx, ty, block_type)
                    # Broadcast block change
                    self.broadcast_block_change(tx, ty, block_type)
                
                elif msg_type == "get_chunk":
                    # Send chunk data
                    cx, cy = data["cx"], data["cy"]
                    chunk = get_chunk(cx, cy)
                    self.send_to_client(client, {
                        "type": "chunk_data",
                        "cx": cx,
                        "cy": cy,
                        "data": chunk
                    })
        
        except Exception as e:
            print(f"Client {player_id} error: {e}")
        finally:
            with self.lock:
                if player_id in self.clients:
                    del self.clients[player_id]
            client.close()
            print(f"Client {player_id} disconnected")

    def receive_from_client(self, client):
        """Receive data from a client"""
        try:
            data = b""
            while True:
                chunk = client.recv(4096)
                if not chunk:
                    return None
                data += chunk
                try:
                    return pickle.loads(data)
                except:
                    continue
        except:
            return None

    def send_to_client(self, client, data):
        """Send data to a client"""
        try:
            client.sendall(pickle.dumps(data))
        except:
            return False
        return True

    def broadcast_players(self):
        """Broadcast all player data to all clients"""
        with self.lock:
            players_data = {}
            for pid, player_info in self.clients.items():
                players_data[pid] = {
                    "x": player_info["x"],
                    "y": player_info["y"],
                    "vel_x": player_info["vel_x"],
                    "vel_y": player_info["vel_y"],
                    "on_ground": player_info["on_ground"]
                }
        
        for pid, player_info in self.clients.items():
            self.send_to_client(player_info["socket"], {
                "type": "players_update",
                "players": players_data
            })

    def broadcast_block_change(self, tx, ty, block_type):
        """Broadcast block change to all clients"""
        for pid, player_info in self.clients.items():
            self.send_to_client(player_info["socket"], {
                "type": "block_change",
                "x": tx,
                "y": ty,
                "block_type": block_type
            })

    def place_block(self, tile_x, tile_y, block_type):
        """Place a block in the world"""
        cx = tile_x // CHUNK_SIZE
        cy = tile_y // CHUNK_SIZE

        chunk = get_chunk(cx, cy)

        lx = tile_x % CHUNK_SIZE
        ly = tile_y % CHUNK_SIZE

        if 0 <= lx < CHUNK_SIZE and 0 <= ly < CHUNK_SIZE:
            chunk[ly][lx] = block_type


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Game Server")
    parser.add_argument("--host", default="0.0.0.0", help="Server host/IP (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5555, help="Server port (default: 5555)")
    args = parser.parse_args()
    
    server = GameServer(host=args.host, port=args.port)
    server.start()
