import microbit
import radio
import music

radio.config(group=1)

name = "kitchen"
clients_seen = []

with open('devices_seen.txt', 'w') as data_file:
    while True:
        details = radio.receive_full()
        if details:
            id, rssi, timestamp = details
            id = str(id, 'utf8')
            if id not in clients_seen:
                if rssi > -40:
                    data_file.write(id + "\n")
                    music.play(music.DADADADUM)
                    clients_seen.append(id)
                    microbit.display.show(microbit.Image.HAPPY)
                    microbit.sleep(1000)
                    microbit.display.clear()

        if microbit.button_a.was_pressed():
            microbit.display.scroll(", ".join(clients_seen))