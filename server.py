import asyncio
import websockets

ip = '0.0.0.0'
port = 8765

print(f'now running server at {ip}:{port}')

async def server(ws, path):
    print(f'connected to {path} from {ws.remote_address}')

    i = 1
    try:
        async for message in ws:
            greeting = f'hello, {message} {i}'
            i += 1
            await ws.send(greeting)
            print(f'send {greeting}')
    except websockets.ConnectionClosedError:
        pass

    print(f'disconnected {ws.remote_address}')

start_server = websockets.serve(server, ip, port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

