import microbit
import radio

radio.config(group=1)
radio.on()

id = "My name"

while True:
    radio.send(id)
