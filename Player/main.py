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
[3:] is merely a workaround.. Need to figure out why it's doing that.
"""

def snake_loop():
    counter = 0
    display.show(Image("00000:06060:90009:06060:00000"))

    while True:
        details = radio.receive_full()
        if details:
            if str(details[0],'utf8')[3:] == "stop":
                break
        if counter == 7500: # breaks after a while if stop signal not detected
            break
        if button_a.was_pressed():
            radio.send("inp_a")
            counter = 0
        if button_b.was_pressed():
            radio.send("inp_b")
            counter = 0
        time.sleep(0.001)
        counter += 1

    speech.say("disconnected")
    display.show(Image("00000:00000:00000:00000:00000"))


while True:
    # if details: ## debugging purposes
    #     display.scroll(str(details[0],'utf8'))
    details = radio.receive_full()
    if details:
        if str(details[0],'utf8')[3:] == id+"_playsnake": # Target_snake sends back id if not in clients_seen
            speech.say("connected")
            snake_loop()
    radio.send(id)
    time.sleep(0.01)
