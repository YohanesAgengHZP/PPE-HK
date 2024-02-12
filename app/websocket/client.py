import asyncio
import websockets

async def send_message():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, WebSocket!")
        response = await websocket.recv()
        print(response)

# Use asyncio.run() to run the coroutine
asyncio.run(send_message())
