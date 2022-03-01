import asyncio
import websockets
import os
import random

ip = '0.0.0.0'
port = 8765

websocket_clients = dict()

async def handle_socket_connection(websocket, path):
    """Handles the whole lifecycle of each client's websocket connection."""
    websocket_clients[path] = websocket
    print(f'New connection from: {websocket.remote_address} ({len(websocket_clients)} total) (path {path})')
    try:
        # This loop will keep listening on the socket until its closed. 
        async for raw_message in websocket:
            if path == '/raspi' and websocket_clients['/phone'] != None:
                await websocket_clients['/phone'].send("wow!!!!" + raw_message)
    except websockets.exceptions.ConnectionClosedError as cce:
        pass
    finally:
        print(f'Disconnected from socket [{id(websocket)}]...')
        websocket_clients[path] = None
        #websocket_clients.remove(websocket)

async def broadcast_random_number(loop):
    """Keeps sending a random # to each connected websocket client"""
    while True:
        for c in websocket_clients:
            num = str(random.randint(10, 99))
            print(f'Sending [{num}] to socket [{id(c)}]')
            await c.send(num)
        await asyncio.sleep(2)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        socket_server = websockets.serve(handle_socket_connection, ip, port)
        print(f'Started socket server: {socket_server} ...')
        loop.run_until_complete(socket_server)
        loop.run_until_complete(broadcast_random_number(loop))
        loop.run_forever()
    finally:
        loop.close()
        print(f"Successfully shutdown [{loop}].")

