# Multiplayer Network Setup Guide

This guide explains how to set up the game to work across multiple devices on a network.

## Prerequisites
- Python 3.8+
- pygame
- Both devices on the same network (LAN) or accessible via internet
- Firewall configured to allow port 5555 (or your chosen port)

## Local Network Setup (Same WiFi/LAN)

### Step 1: Find Server Machine IP Address

**Windows:**
```powershell
ipconfig
```
Look for "IPv4 Address" - typically looks like `192.168.x.x` or `10.0.x.x`

**Mac/Linux:**
```bash
ifconfig
```
Look for "inet" address

### Step 2: Start the Server

On the machine that will host the server:
```bash
python server.py
```

The server will start on `0.0.0.0:5555` and accept connections from any device.

**Output:**
```
Server started on 0.0.0.0:5555
```

### Step 3: Connect Clients

On any other device on the same network:
```bash
python 2dminecraft_multiplayer.py --host <SERVER_IP_ADDRESS>
```

**Example:**
```bash
python 2dminecraft_multiplayer.py --host 192.168.1.100
```

## Same Machine Setup (Local Play)

To run multiple clients on the same machine:

**Terminal 1 (Server):**
```bash
python server.py
```

**Terminal 2 (Client 1):**
```bash
python 2dminecraft_multiplayer.py
```

**Terminal 3 (Client 2):**
```bash
python 2dminecraft_multiplayer.py --host 127.0.0.1
```

## Custom Port (Optional)

If port 5555 is already in use, use a different port:

**Server:**
```bash
python server.py --port 5556
```

**Client:**
```bash
python 2dminecraft_multiplayer.py --host <SERVER_IP> --port 5556
```

## Internet Play (Advanced)

To play over the internet (not recommended without proper security):

1. **Port Forwarding**: Forward port 5555 (or custom) on your router to your server machine
2. **Dynamic DNS**: If your IP changes, use a service like No-IP or DuckDNS
3. **Connect with Public IP**: Share your public IP with other players

```bash
python 2dminecraft_multiplayer.py --host <YOUR_PUBLIC_IP>
```

## Troubleshooting

### "Connection refused" Error
- Verify the server is running with `python server.py`
- Check firewall settings allow port 5555
- Ensure you're using the correct IP address

### "Connection timeout" Error
- Verify both devices are on the same network
- Check the server machine's IP address again
- Make sure no firewall is blocking the connection

### Server runs but clients won't connect
- Use `0.0.0.0` binding (default) so server accepts external connections
- Check Windows/Mac firewall to allow the Python script

### Network lag issues
- Move closer to the router
- Close bandwidth-heavy applications
- Reduce network update interval in the code (default: 5 frames)

## Checking Connections

**On Server:** The server will print connection messages:
```
Connection from ('192.168.1.105', 54321)
Connected as Player 0
```

**On Client:** You'll see:
```
Connected as Player 1
Loaded X block definitions
Loaded X item definitions
Game data loaded successfully
```

## Performance Tips

1. **Reduce Update Frequency** - Edit client code, increase `network_update_interval` from 5 to 10+
2. **Reduce Broadcast Frequency** - Edit server code, increase `broadcast_interval` from 0.05 to 0.1+
3. **Limit Players** - More players = more network traffic
4. **Close Other Programs** - Free up bandwidth for the game

## Default Settings

- **Server Port:** 5555
- **Server Binding:** 0.0.0.0 (accepts all connections)
- **Client Default Host:** 127.0.0.1 (localhost)
- **Network Update Rate:** Every 5 frames (~12 updates/sec)
- **Broadcast Rate:** 20 times/sec (50ms intervals)

## Security Notes

⚠️ This is a development game, not production-grade. For internet play:
- Don't expose sensitive data
- Consider using a VPN
- Add authentication if deploying widely
