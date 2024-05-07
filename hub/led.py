import RPi.GPIO as GPIO
from time import sleep

red_pin = 13
green_pin = 19
blue_pin = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)

def set(red, green, blue):
    GPIO.output(red_pin, red)
    GPIO.output(green_pin, green)
    GPIO.output(blue_pin, blue)


def off():
    set(0, 0, 0)


def color(color):
    if color == "red":
        set(1, 0, 0)
    elif color == "green":
        set(0, 1, 0)
    elif color == "blue":
        set(0, 0, 1)
    elif color == "purple":
        set(1, 0, 1)
    elif color == "yellow":
        set(1, 1, 0)
    elif color == "cyan":
        set(0, 1, 1)
    elif color == "white":
        set(1, 1, 1)
    else:
        set(0, 0, 0)

def turn_on_for_duration(c, duration):
    print("Turning on")
    color(c)
    sleep(duration)
    print("Turning off")
    off()


def cleanup():
    GPIO.cleanup()
