import RPi.GPIO as GPIO
import asyncio
from sockets.sdk import WebSocketClient
import led  # Import the led module
import time

# Button setup
button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Constants for button press types
LONG_PRESS_MIN = 1.5
DOUBLE_PRESS_INTERVAL = 0.3
DEBOUNCE_TIME = 0.05

# Time tracking
last_press_time = 0
press_start_time = None
long_press_triggered = False
last_press_was_double = False
button_state = GPIO.input(button_pin)

# Initialize the WebSocket client
ws_client = WebSocketClient("ws://localhost:8765")

async def short_press():
    print("Short Press Detected")
    await ws_client.send("Short Press")

async def long_press():
    print("Long Press Detected")
    await ws_client.send("Long Press")

async def double_press():
    print("Double Press Detected")
    await ws_client.send("Double Press")

async def check_button_state():
    global button_state, press_start_time, long_press_triggered
    current_state = GPIO.input(button_pin)
    if current_state != button_state:
        await asyncio.sleep(DEBOUNCE_TIME)  # Non-blocking debounce
        current_state = GPIO.input(button_pin)

    if current_state == False and button_state == True:
        led.color("purple")  # Turn on purple LED when button is pressed
        press_start_time = time.time()
        long_press_triggered = False
    elif current_state == True and button_state == False:
        led.off()  # Turn off LED when button is released
        await handle_button_release()
    button_state = current_state

async def handle_button_release():
    global last_press_time, last_press_was_double, press_start_time, long_press_triggered
    press_duration = time.time() - press_start_time
    if not long_press_triggered:
        if press_duration >= LONG_PRESS_MIN:
            await long_press()
            long_press_triggered = True
        else:
            await handle_short_or_double_press()
    press_start_time = None

async def handle_short_or_double_press():
    global last_press_time, last_press_was_double
    if time.time() - last_press_time < DOUBLE_PRESS_INTERVAL and not last_press_was_double:
        await double_press()
        last_press_was_double = True
    elif not last_press_was_double:
        await short_press()
    else:
        last_press_was_double = False
    last_press_time = time.time()

async def main():
    print(ws_client)
    await ws_client.connect()
    try:
        while True:
            await check_button_state()
            await asyncio.sleep(0.02)
    finally:
        await ws_client.disconnect()
        led.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
