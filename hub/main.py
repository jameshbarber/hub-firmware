import threading
import button
import time
import led
import uinput
from rfid import read_rfid  # Import the RFID reading function
device = uinput.Device([uinput.KEY_S, uinput.KEY_L, uinput.KEY_D, uinput.KEY_SPACE, uinput.KEY_G])

def btn_callback(type: str):

    print("Button fetched")

    if (type == 'press'):
        led.color("purple")
        print('Press detected')
    elif (type == 'release'):
        led.off()
        print('Release detected')
    if (type == 'short'):
        # led.turn_on_for_duration("blue", 0.2)
        device.emit_click(uinput.KEY_G)  # Emit 's' for short press
        print('Short press detected')
    elif (type == 'long'):
        device.emit_click(uinput.KEY_L)  # Emit 'l' for long press
        print('Long press detected')
    elif (type == 'double'):    
        print('Double press detected')
    else:
        print('Unknown press detected')



def rfid_thread_function():
    while True:
        success, id, text = read_rfid()
        if success:
            led.color("green")  # Or any other indication you want
            time.sleep(0.2)
            led.off()

        time.sleep(1)  # Wait a bit before trying to read again


def button_monitor():
    while True:
        button.check_button_state(btn_callback)
        time.sleep(0.02)  # Short sleep to reduce CPU usage

if __name__ == "__main__":
    # led.setup()
    # Start the RFID reading in a separate thread
    rfid_thread = threading.Thread(target=rfid_thread_function)
    rfid_thread.daemon = True
    rfid_thread.start()

    # Start the button handling in another separate thread
    button_thread = threading.Thread(target=button_monitor)
    button_thread.daemon = True
    button_thread.start()

    print("Started RFID and button threads.")
    led.color("green")
    try:
        while True:
            # Main loop does nothing; it just keeps the script running
            time.sleep(10)
    except KeyboardInterrupt:
        print("Program terminated.")
