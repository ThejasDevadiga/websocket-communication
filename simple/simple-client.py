import asyncio
 
import websockets
 
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def test():
    async with websockets.connect('ws://192.168.137.24:80/ws') as websocket:
        await websocket.send("00")
        while True:
            try:

                await websocket.send(input("Enter any text :"))
                response = await websocket.recv()
                print(response)
            except:
                websockets.connect('ws://192.168.137.24:80/ws')
            
asyncio.get_event_loop().run_until_complete(test())
 
# asyncio.run(test())