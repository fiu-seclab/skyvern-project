import asyncio

import websockets


async def main():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send("run")
        recv = await websocket.recv()
        print(recv)


asyncio.run(main())
