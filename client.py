import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://gang-and-friends.com:8765/raspi') as ws:
        name = input('input yoru name: ')
        await ws.send(name)
        print(f'send {name}')

        greeting = await ws.recv()
        print(f'recv {greeting}')

asyncio.get_event_loop().run_until_complete(hello())
