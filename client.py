import asyncio
import websockets

#url = 'ws://gang-and-friends.com:8765/raspi'
url = 'ws://localhost:8765/raspi'

async def hello():
    async with websockets.connect(url) as ws:
        name = input('input yoru name: ')
        ba = bytearray(name, 'utf-8')
        await ws.send(ba)
        print(f'send {name}')

asyncio.get_event_loop().run_until_complete(hello())
