import asyncio
import websockets

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri + "?role=input"  # Append role query to the URI
        self.connection = None

    async def connect(self):
        self.connection = await websockets.connect(self.uri)
        print(f"Connected to WebSocket at {self.uri}")

    async def send(self, message):
        if self.connection:
            await self.connection.send(message)
            print(f"Sent message: {message}")
        else:
            print("Connection not established")

    async def receive_messages(self, message_handler=None):
        try:
            async for message in self.connection:
                print(f"Received message: {message}")
                if message_handler:
                    message_handler(message)
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            print("Disconnected from WebSocket")

# Example usage
async def main():
    client = WebSocketClient("ws://localhost:8765")
    await client.connect()
    await client.send("Hello from input client!")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
