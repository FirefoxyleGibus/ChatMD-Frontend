import asyncio
import websockets
import json

CONNECTIONS = set()

async def register(websocket):
    CONNECTIONS.add(websocket)
    message = await websocket.recv()
    print(f"<- {message}")
    await broadcast(CONNECTIONS, json.dumps({"content":message,"username":"SERVER"}))
    print(f"-> [\"content\":{message}, \"username\":\"SERVER\"]")
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)

async def broadcast(clients, message):
    for websocket in clients:
        try:
            await websocket.send(message)
        except websockets.ConnectionClosed:
            pass

async def main():
    async with websockets.serve(register, "localhost", 8081):
        await asyncio.Future()


if __name__ == "__main__":
    print("!! SERVER IS UP !!")
    asyncio.run(main())