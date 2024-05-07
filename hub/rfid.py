import asyncio
from mfrc522 import SimpleMFRC522
from RPi import GPIO
from sockets.sdk import WebSocketClient

async def read_rfid_and_send():
    reader = SimpleMFRC522()
    client = WebSocketClient("ws://localhost:8765")  # Adjust the URI as needed
    
    await client.connect()
    
    try:
        while True:
            id, text = reader.read()  # This blocks until an RFID tag is read
            print(f"RFID read: ID: {id}, Text: {text}")
            await client.send(f"RFID ID: {id}, Text: {text}")
            await asyncio.sleep(1)  # Sleep for a short while to avoid bombarding the server
    except Exception as e:
        print("Error reading RFID or sending data:", e)
    finally:
        GPIO.cleanup()  # Clean up GPIO to ensure we're not leaving anything hanging
        await client.disconnect()  # Disconnect the WebSocket connection gracefully

async def main():
    await read_rfid_and_send()

if __name__ == "__main__":
    asyncio.run(main())
