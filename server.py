import asyncio
import websockets

ip = '0.0.0.0'
port = 8765

print(f'now running server at {ip}:{port}')

async def server(ws, path):
    print(f'connected to {path} from {ws.remote_address}')

    i = 1
    while True:
        try:
            name = await ws.recv()
            print(f'recv {name}')

            greeting = f'hello, {name} {i}'
            i += 1
            await ws.send(greeting)
            print(f'send {greeting}')
        except websockets.ConnectionClosedOK:
            print(f'{ws.remote_address} disconnected')
            break

start_server = websockets.serve(server, ip, port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

