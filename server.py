import asyncio
import os
import websockets

clients = set()

async def handler(ws):
    clients.add(ws)
    print(f"Client connected. Total: {len(clients)}")

    try:
        async for message in ws:
            print("Message:", message)

            disconnected = []
            for client in clients:
                if client != ws:
                    try:
                        await client.send(message)
                    except websockets.ConnectionClosed:
                        disconnected.append(client)

            for client in disconnected:
                clients.discard(client)

    finally:
        clients.discard(ws)
        print(f"Client disconnected. Total: {len(clients)}")

async def main():
    port = int(os.environ.get("PORT", 10000))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"Server running on port {port}")
        await asyncio.Future()

asyncio.run(main())
