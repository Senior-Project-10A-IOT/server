import asyncio
import websockets

url = 'ws://gang-and-friends.com:8765/raspi'
#url = 'ws://localhost:8765/raspi'

async def hello():
    ok = await websockets.connect(url + '2')
    async with websockets.connect(url) as ws:
        name = input('input yoru name: ')
        await ws.send(name)
        print(f'send {name}')

asyncio.get_event_loop().run_until_complete(hello())
