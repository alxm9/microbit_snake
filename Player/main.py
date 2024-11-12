import microbit
import radio
import speech
import time
from microbit import button_a, button_b

radio.on()
radio.config(group=1, queue=1) # queue=1 so input doesn't get flooded

id = "My name"

def press_checker():
    if button_a.was_pressed():
        radio.send("a")
    if button_b.was_pressed():
        radio.send("b")

while True:
    press_checker()