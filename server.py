import asyncio
import websockets

IP = '0.0.0.0'
PORT = 8765
PHONE_PATH = '/phone'
PI_PATH = '/raspi'

phone_socket = None

async def handle_socket_connection(websocket, path):
    global phone_socket
    print(f'New connection from: {websocket.remote_address} (path {path})')

    if path == PHONE_PATH:
        phone_socket = websocket

    try:
        async for raw_message in websocket:
            print('recv', phone_socket, path)
            if phone_socket != None and path == PI_PATH:
                if type(raw_message) == str:
                    print('yes')
                    await phone_socket.send("from server: " + raw_message)
                elif type(raw_message) == bytes:
                    print('no')
                    await phone_socket.send(raw_message)

    except websockets.exceptions.ConnectionClosedError as cce:
        pass

    finally:
        print(f'Disconnected from socket [{id(websocket)}]...')
        if path == PHONE_PATH:
            phone_socket = None

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        socket_server = websockets.serve(handle_socket_connection, IP, PORT)
        print(f'Started socket server: {socket_server} ...')
        loop.run_until_complete(socket_server)
        loop.run_forever()
    finally:
        loop.close()
        print(f"Successfully shutdown [{loop}].")

