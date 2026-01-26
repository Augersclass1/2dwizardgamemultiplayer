import socket
import threading
import pickle
import random
import math
import argparse
import struct
import sys
import os
import time

# Add current directory to path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_data import BLOCKS, ITEMS, AIR, DIRT_TILE, STONE_TILE, GRASS_TILE, SAND_TILE, WOOD_TILE, LEAF_TILE, GRAVEL_TILE, COAL_ORE_TILE, COPPER_ORE_TILE, OBSIDIAN_TILE, SNOW_TILE, ICE_TILE, DARK_OAK_WOOD_TILE, DARK_OAK_LEAF_TILE, CACTUS_TILE, GAMEVERSION

# =====================
# CONSTANTS
# =====================
TILE_SIZE = 40
CHUNK_SIZE = 16

# =====================
# WORLD GENERATION
# =====================
world = {}

def hash_function(x):
    """True random hash without sine - uses bit manipulation"""
    x = int(x)
    x = (x ^ 61) ^ (x >> 13)
    x = x * 2654435769
    x = x ^ (x >> 16)
    return (x & 0x7fffffff) / 2147483647.0

def linear_interpolate(t):
    """Linear interpolation - less smooth, more jagged"""
    return t

def value_noise(x, scale=1.0):
    """Generate value noise with less smoothing for more randomness"""
    x_scaled = x / scale
    xi = math.floor(x_scaled)
    xf = x_scaled - xi
    
    # Hash based noise values
    n0 = hash_function(xi)
    n1 = hash_function(xi + 1)
    
    # Less smooth interpolation for more randomness
    u = linear_interpolate(xf)
    return n0 * (1 - u) + n1 * u

def fractal_noise(x, octaves=6, persistence=0.5, scale=50):
    """Generate fractal brownian motion for bumpy, random terrain"""
    total = 0
    amplitude = 1.0
    frequency = 1.0
    max_amplitude = 0
    
    for i in range(octaves):
        # Add offset to each octave for more randomness
        offset = i * 10000
        total += value_noise(x * frequency + offset, scale / frequency) * amplitude
        max_amplitude += amplitude
        amplitude *= persistence
        frequency *= 2.0
    
    return (total / max_amplitude) if max_amplitude > 0 else 0
# !!!!!!! really important the below needs to be fixed so that the biome actually changes
def get_biome(global_x):
    """Determine biome type with smooth transitions"""
    # Large scale noise for biome regions - less interpolation for more variation
    biome_noise = value_noise(global_x, 300) * 100
    biome_noise += value_noise(global_x + 5000, 150) * 50
    
    # Determine biome with smooth ranges
    if biome_noise > 110:
        return "desert"
    elif biome_noise > 70:
        return "plains"
    elif biome_noise > 30:
        return "forest"
    elif biome_noise > -10:
        return "mountain"
    else:
        return "ice_plains"

def get_height(global_x):
    """Get terrain height with heavy randomness and bumps"""
    biome = get_biome(global_x)
    
    # Use fractal noise for bumpy, chaotic terrain
    fractal = fractal_noise(global_x, octaves=5, persistence=0.6, scale=30)
    
    if biome == "mountain":
        # Mountains: very bumpy and chaotic
        return int(13 + fractal * 12)
    elif biome == "desert":
        # Desert: mostly flat with occasional bumps
        return int(9 + fractal * 1.5)
    elif biome == "ice_plains":
        # Ice: very flat but with small random bumps
        return int(10 + fractal * 0.8)
    elif biome == "plains":
        # Plains: gently rolling with randomness
        return int(9 + fractal * 3)
    else:
        # Forest: moderately bumpy
        return int(9 + fractal * 5)

def generate_tree(tiles, x, y, biome="forest"):
    """Generate a tree based on biome"""
    if biome == "forest":
        # Normal oak tree
        height = random.randint(4, 6)
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
    
    elif biome == "mountain":
        # Tall dark oak tree
        height = random.randint(6, 9)
        for i in range(height):
            if y - i >= 0:
                tiles[y - i][x] = DARK_OAK_WOOD_TILE
        
        leaf_start = y - height
        for lx in range(-2, 3):
            for ly in range(-3, 3):
                if abs(lx) + abs(ly) < 5:
                    tx = x + lx
                    ty = leaf_start + ly
                    if 0 <= tx < CHUNK_SIZE and 0 <= ty < CHUNK_SIZE:
                        if tiles[ty][tx] == AIR:
                            tiles[ty][tx] = DARK_OAK_LEAF_TILE
    
    elif biome == "desert":
        # Cactus instead of trees
        height = random.randint(2, 4)
        for i in range(height):
            if y - i >= 0:
                tiles[y - i][x] = CACTUS_TILE

def generate_chunk(cx, cy):
    """Generate a chunk with biome-specific features"""
    tiles = [[AIR for _ in range(CHUNK_SIZE)] for _ in range(CHUNK_SIZE)]
    
    for y in range(CHUNK_SIZE):
        for x in range(CHUNK_SIZE):
            global_x = cx * CHUNK_SIZE + x
            global_y = cy * CHUNK_SIZE + y
            ground_height = get_height(global_x)
            biome = get_biome(global_x)
            
            if global_y > ground_height:
                # Surface block
                if global_y == ground_height + 1:
                    if biome == "desert":
                        tiles[y][x] = SAND_TILE
                    elif biome == "ice_plains":
                        tiles[y][x] = SNOW_TILE if random.random() < 0.8 else ICE_TILE
                    elif biome == "mountain":
                        tiles[y][x] = STONE_TILE if random.random() < 0.6 else GRAVEL_TILE
                    else:  # plains and forest
                        tiles[y][x] = GRASS_TILE
                
                # Underground blocks
                elif global_y > ground_height + 4:
                    if biome == "desert":
                        tiles[y][x] = SAND_TILE if random.random() < 0.7 else GRAVEL_TILE
                    elif biome == "ice_plains":
                        tiles[y][x] = ICE_TILE
                    else:
                        # Stone with ores
                        if random.random() < 0.05:
                            tiles[y][x] = COAL_ORE_TILE
                        elif random.random() < 0.02:
                            tiles[y][x] = COPPER_ORE_TILE
                        elif random.random() < 0.01 and global_y > ground_height + 10:
                            tiles[y][x] = OBSIDIAN_TILE
                        else:
                            tiles[y][x] = STONE_TILE if random.random() < 0.8 else DIRT_TILE
                else:
                    tiles[y][x] = DIRT_TILE

    # Add trees and vegetation
    for x in range(CHUNK_SIZE):
        global_x = cx * CHUNK_SIZE + x
        ground_y = get_height(global_x)
        local_y = ground_y - cy * CHUNK_SIZE
        biome = get_biome(global_x)
        
        if 0 <= local_y < CHUNK_SIZE:
            # Forest biome has more trees
            if biome == "forest" and random.random() < 0.06:
                generate_tree(tiles, x, local_y, biome)
            # Mountain biome has some trees
            elif biome == "mountain" and random.random() < 0.03:
                generate_tree(tiles, x, local_y, biome)
            # Desert has cacti
            elif biome == "desert" and random.random() < 0.05:
                generate_tree(tiles, x, local_y, biome)

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
        # Optimization: Throttle broadcast frequency
        self.last_broadcast_time = 0
        self.broadcast_interval = 0.05  # Broadcast every 50ms instead of every message

    def get_local_ip(self):
        """Get the local IP address of this machine"""
        try:
            # Create a temporary socket to determine the local IP
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Connect to a public DNS server (doesn't actually send data)
            temp_socket.connect(("8.8.8.8", 80))
            local_ip = temp_socket.getsockname()[0]
            temp_socket.close()
            return local_ip
        except:
            # Fallback to localhost if unable to determine
            return "127.0.0.1"

    def start(self):
        """Start the server"""
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            
            # Display server information
            print("=" * 50)
            print("MULTIPLAYER WIZARD GAME - SERVER")
            print("=" * 50)
            print(f"Server started on {self.host}:{self.port}")
            
            # Show the IP address clients should use
            local_ip = self.get_local_ip()
            print(f"\n📡 CLIENTS SHOULD CONNECT TO:")
            print(f"   IPv4 Address: {local_ip}:{self.port}")
            print(f"\n   Command:")
            print(f"   python 2dminecraft_multiplayer.py --host {local_ip}")
            print("=" * 50 + "\n")
            
            while True:
                client, addr = self.server.accept()
                print(f"Connection from {addr}")
                
                with self.lock:
                    player_id = self.player_id_counter
                    self.player_id_counter += 1
                
                # Send player ID using proper protocol
                self.send_to_client(client, player_id)
                
                # Now check version
                try:
                    client.settimeout(5)
                    version_check = self.receive_from_client(client)
                    
                    if not version_check or version_check.get("type") != "version_check":
                        print(f"  ❌ Invalid version check from {addr}")
                        self.send_to_client(client, {
                            "type": "connection_rejected",
                            "reason": "Invalid protocol"
                        })
                        client.close()
                        continue
                    
                    client_version = version_check.get("version")
                    if client_version != GAMEVERSION:
                        print(f"  ❌ Version mismatch from {addr}: client={client_version}, server={GAMEVERSION}")
                        self.send_to_client(client, {
                            "type": "connection_rejected",
                            "reason": f"Version mismatch. Server: {GAMEVERSION}, Your version: {client_version}"
                        })
                        client.close()
                        continue
                    
                    print(f"  ✓ Version check passed ({GAMEVERSION})")
                except Exception as e:
                    print(f"  ❌ Error during version check: {e}")
                    client.close()
                    continue
                
                # Send version check acknowledgment
                self.send_to_client(client, {
                    "type": "version_check_ok"
                })
                
                # Send block definitions
                self.send_to_client(client, {
                    "type": "block_definitions",
                    "blocks": BLOCKS
                })
                
                # Send item definitions
                self.send_to_client(client, {
                    "type": "item_definitions",
                    "items": ITEMS
                })
                
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
        """Receive data from a client with length prefix"""
        try:
            # Receive 4-byte length prefix
            length_data = b""
            while len(length_data) < 4:
                chunk = client.recv(4 - len(length_data))
                if not chunk:
                    return None
                length_data += chunk
            
            message_length = struct.unpack("I", length_data)[0]
            
            # Receive exact number of bytes for message
            data = b""
            while len(data) < message_length:
                chunk = client.recv(message_length - len(data))
                if not chunk:
                    return None
                data += chunk
            
            return pickle.loads(data)
        except Exception as e:
            print(f"Receive error: {e}")
            return None

    def send_to_client(self, client, data):
        """Send data to a client with length prefix"""
        try:
            serialized = pickle.dumps(data)
            # Send length prefix (4 bytes) followed by data
            client.sendall(struct.pack("I", len(serialized)) + serialized)
        except Exception as e:
            print(f"Send error: {e}")
            return False
        return True

    def broadcast_players(self):
        """Broadcast all player data to all clients (throttled)"""
        current_time = time.time()
        # Only broadcast at intervals to reduce network traffic
        if current_time - self.last_broadcast_time < self.broadcast_interval:
            return
        
        self.last_broadcast_time = current_time
        
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
