import microbit
import radio
import speech
import time
from microbit import button_a, button_b, display, Image

radio.on()
radio.config(group=1, queue=1, power=7) # queue=1 so input doesn't get flooded

id = "test"

"""
For some reason str(details[0],'utf8') returns everything with "???" attached at the beginning. ( "???whatever" )
[3:] is merely a workaround. Need to figure out why it's doing that.
"""

def snake_loop():
    counter = 0
    display.show(Image.HAPPY) # placeholder
    while True:
        details = radio.receive_full()
        if details:
            if str(details[0],'utf8')[3:] == "stop": #WIP
                speech.say("broken")
                return
        if counter == 1000: # breaks after a while if stop signal not detected
            speech.say("broken")
            return
        if button_a.is_pressed():
            radio.send("a")
            counter = 0
        elif button_b.is_pressed():
            radio.send("b")
            counter = 0
        time.sleep(0.01)
        counter += 1

while True:
    details = radio.receive_full()
    if details:
        if str(details[0],'utf8')[3:] == id+"_playsnake": # Target_snake sends back id if not in clients_seen
            speech.say("connected")
            snake_loop()
    radio.send(id)
    time.sleep(0.1)
