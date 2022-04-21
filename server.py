import asyncio
import websockets
import json

IP = '0.0.0.0'
PORT = 8765
PHONE_PATH = '/phone'
PI_PATH = '/raspi'

phone_socket = None
pi_socket = None

async def from_phone(message):
    global pi_socket
    print(f'message from phone: \'{message}\'')

    await pi_socket.send(message)

async def from_pi(message):
    global phone_socket
    print(f'message from pi: \'{message}\'')
    await phone_socket.send(message)

async def handle_socket_connection(websocket, path):
    global phone_socket
    global pi_socket
    print(f'New connection from: {websocket.remote_address} (path {path})')

    if path == PHONE_PATH:
        phone_socket = websocket
    if path == PI_PATH:
        pi_socket = websocket

    try:
        async for message in websocket:
            # TODO send this message from the pi
            if path == PHONE_PATH and message == 'arm':
                print('replying with armed')
                await phone_socket.send('armed')
            if path == PHONE_PATH and message == 'disarm':
                print('replying with disarmed')
                await phone_socket.send('disarmed')

            if phone_socket != None and pi_socket != None:
                if path == PHONE_PATH:
                    await from_phone(message)
                elif path == PI_PATH:
                    await from_pi(message)
            else:
                reason = 'idk why'
                if phone_socket == None:
                    reason = 'phone not connected'
                elif pi_socket == None:
                    reason = 'pi not connected'
                print(f'dropped message from {path}, {reason}')

    except websockets.exceptions.ConnectionClosedError as cce:
        pass

    finally:
        print(f'Disconnected from socket {path}...')
        if path == PHONE_PATH:
            phone_socket = None
        if path == PI_PATH:
            pi_socket = None

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

