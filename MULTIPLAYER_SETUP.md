# Multiplayer Game Setup

Your game now supports multiplayer! Here's how to use it:

## Files Added:
- **server.py** - Game server that manages world state and player positions
- **network.py** - Networking utilities for client-server communication
- **2dminecraft_multiplayer.py** - Multiplayer game client

## How to Run:

### 1. Start the Server (on the host machine)
```bash
python server.py
```
You should see: `Server started on localhost:5555`

### 2. Start Clients (each player runs this)
```bash
python 2dminecraft_multiplayer.py
```

Each client will:
- Connect to the server
- Receive a unique Player ID
- Display other players in red
- Your player is displayed in blue

## Features:

- **Real-time multiplayer**: See other players moving in real-time
- **Shared world**: All block placements are synchronized across all players
- **Server-authoritative**: The server manages the world state
- **Chunk loading**: Chunks are loaded on-demand from the server
- **Player tracking**: Each player's position is synced and displayed

## Controls:
- **A/D** - Move left/right
- **W** - Jump
- **Right Click** - Place blocks
- **Left Click** - Break blocks
- **F3** - Toggle debug info
- **ESC** - Quit

## Connection Settings:
If you want to play over the network instead of localhost:

Edit `2dminecraft_multiplayer.py` line ~359:
```python
if not network.connect("192.168.x.x", 5555):  # Replace with server IP
```

Also edit `server.py` line ~115 if needed to bind to a specific interface.

## Notes:
- The server must be running before any clients connect
- Multiple clients can connect simultaneously
- All world changes are persisted in the server's `world` dictionary
- The game generates terrain procedurally - no seed sync yet (terrain may vary slightly)

Enjoy your multiplayer wizard game!
