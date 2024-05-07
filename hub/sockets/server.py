import asyncio
import websockets

input_clients = set()
output_clients = set()

async def handler(websocket, path):
    print(f"New connection: {path}")
    
    # Correctly parse the role from the query parameter
    role = path.split('?')[1].split('=')[1] if '?' in path else 'input'
    
    if role == 'output':
        output_clients.add(websocket)
        print("Output client connected")
        await websocket.send("Hello, output client!")  # Greet newly connected output clients
    else:
        input_clients.add(websocket)
        print("Input client connected")

    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Only broadcast messages received from input clients to output clients
            if websocket in input_clients:
                await broadcast_to_outputs(message)
    finally:
        # Properly remove the websocket from the appropriate set upon disconnection
        input_clients.discard(websocket)
        output_clients.discard(websocket)
        print(f"Client disconnected")

async def broadcast_to_outputs(message):
    for client in output_clients:
        try:
            await client.send(message)
            print("Message broadcasted to output client.")
        except websockets.exceptions.ConnectionClosed:
            output_clients.remove(client)
            print("Output connection closed and client removed")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started at ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
