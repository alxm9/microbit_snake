################## REFERENCE
# import microbit
# import radio
# import music

# radio.on()
# radio.config(group=1)

# name = "kitchen"
# clients_seen = []

# with open('devices_seen.txt', 'w') as data_file:
#     while True:
#         details = radio.receive_full()
#         if details:
#             id, rssi, timestamp = details
#             id = str(id, 'utf8')
#             if id not in clients_seen and id not in ["a","b"]:
#                 if rssi > -40:
#                     data_file.write(id + "\n")
#                     music.play(music.DADADADUM)
#                     clients_seen.append(id)
#                     microbit.display.show(microbit.Image.HAPPY)
#                     microbit.sleep(1000)
#                     microbit.display.clear()

#         if microbit.button_a.was_pressed():
#             microbit.display.scroll(", ".join(clients_seen))

from microbit import button_a, button_b, display, Image
import speech
import time
import radio
import random

radio.on()
radio.config(group=1, queue=1)

name = "whatever"
clients_seen = []

ledmap = [
    [ 0,0,0,0,0 ],
    [ 0,0,0,0,0 ],
    [ 0,0,0,0,0 ],
    [ 0,0,0,0,0 ],
    [ 0,0,0,0,0 ]
]

class Snake:
    def __init__(self):
        self.name = False
        self.body_dict = { # y, x
            "piece_1": [0,0] # Starting off with one piece only
        #   "piece_2": [0,1]
        #   "piece_....
        } # Holds the pieces of the body and the coordinates of each on the ledmap
        self.direction = ["right","down","left","up"] # index 0 is the current direction
        self.time_interval = 0.65 #time.sleep
        self.alive = True
        self.steered = False # If you've already steered this turn
       # self.prev_location = # previous location of last piece

    def change_direction(self, button):
        if button == "b": # clockwise
            self.direction = [self.direction[1],self.direction[2],self.direction[3],self.direction[0]]
        else: # counter-clockwise
            self.direction = [self.direction[3],self.direction[0],self.direction[1],self.direction[2]]
            
    def move(self): # Reverse iteration through self.body_dict. every piece takes the coordinates of the one above them in the body, and piece_1 moves according to direction
        #lets start off with piece 1 moving only

        dy_dx = {
            "right": [0,1],
            "left": [0,-1],
            "up": [-1,0],
            "down": [1,0]
        }[self.direction[0]]

        # If walls are touched you die
        if ( self.body_dict["piece_1"][0] + dy_dx[0] ) not in range(0,5):
            self.alive = False
            return
        if ( self.body_dict["piece_1"][1] + dy_dx[1] ) not in range(0,5):
            self.alive = False
            return

        # If piece_1 touches a body part, you die
        for number in range(len(self.body_dict),1,-1):
            if self.body_dict["piece_{0}".format(number)][0] == self.body_dict["piece_1"][0] + dy_dx[0]:
                if self.body_dict["piece_{0}".format(number)][1] == self.body_dict["piece_1"][1] + dy_dx[1]:
                    self.alive = False

        ### check location piece_1 is moving to in advance to determine if it meets fruit
        if ( self.body_dict["piece_1"][0] + dy_dx[0] ) == fruit.location[0]:
            if ( self.body_dict["piece_1"][1] + dy_dx[1] ) == fruit.location[1]:
                self.extend_body()
                speech.say("chomp")
                fruit.change_location()

        # location of every piece replaced with its parent's location. piece_5 to piece_4, piece_4 to piece_3...
        for number in range(len(self.body_dict),1,-1):
            son = "piece_{0}".format(number)
            parent = "piece_{0}".format(number-1)
            self.body_dict[son][0] = self.body_dict[parent][0]
            self.body_dict[son][1] = self.body_dict[parent][1]
        self.body_dict["piece_1"][0] += dy_dx[0] #dy #Piece_1's position is dictated by dy_dx
        self.body_dict["piece_1"][1] += dy_dx[1] #dx

    def extend_body(self): #
        y_coord = self.body_dict["piece_1"][0]
        x_coord = self.body_dict["piece_1"][1]

        self.body_dict["piece_{0}".format(len(self.body_dict)+1)] = [y_coord,x_coord]

class Edible:
    def __init__(self):
        self.location = [3,3]

    def change_location(self):
        old_location = [self.location[0],self.location[1]]
        self.location = [random.randint(0,4),random.randint(0,4)]
        if self.location == old_location: # ensures different location than previously
            self.change_location()
            return
        for key in player.body_dict: # ensures it doesn't get placed on body parts
            if player.body_dict[key] == self.location:
                self.change_location()

player = Snake()
fruit = Edible()

def clear_map(ledmap):
    for row in ledmap:
        for index, column in enumerate(row):
            row[index] = 0

def check_input():
    details = [radio.receive_full() for i in range(30)] # Radio signal filter
    for detail in details:
        if player.steered == False and detail:
            id, rssi, timestamp = detail
            # display.scroll(str(id,"utf8"))
            if str(id,"utf8")[-5:] in ["inp_a","inp_b"]: ## to fix
                if str(id,"utf8")[-1] == "a":
                    player.change_direction("a")
                if str(id,"utf8")[-1] == "b":
                    player.change_direction("b")
                player.steered = True
                return

def refresh_display(): # Converts the ledmap into a string that can be passed to display.show. String is in format "00000:00000:00000:00000:00000"
    for piece in player.body_dict: #
        ledmap[player.body_dict[piece][0]][player.body_dict[piece][1]] = 9
    ledmap[fruit.location[0]][fruit.location[1]] = 9
    imgstring = ":".join("".join(str(item) for item in ledlist) for ledlist in ledmap)
    output = Image(imgstring)
    
    display.show(output)

def restart_game():
    fruit.location = [3,3]
    player.body_dict = {"piece_1": [0,0]}
    player.alive = True
    player.direction = ["right","down","left","up"]
    clear_map(ledmap)
    refresh_display()


def gameloop():
    while True:
        speech.say("start")
        while (player.name not in clients_seen) and player.alive: # Game loop
            clear_map(ledmap)
            check_input()
            time.sleep(player.time_interval)
            check_input() # checking input immediately before and after time.sleep makes it more consistent
            player.move()
            player.steered = False # prevents oversteering
            refresh_display()

            if len(player.body_dict) >= 5: # if score >= 5
                clients_seen.append(player.name)
                speech.say("gee gee")
                player.name = False
                player.alive = True 
                send_stop_signal()
                restart_game()
                display.show(Image("00000:00000:00000:00000:00000")) 
                return
            
        if (len(player.body_dict) == 1) and player.body_dict["piece_1"] == [0,4]:
            speech.say("disconnected")
            send_stop_signal()
            restart_game()
            display.show(Image("00000:00000:00000:00000:00000"))
            time.sleep(2)
            return
 
        restart_game()

def player_checker(detail):
    id = str(detail[0],'utf8')[3:]
    if id in ["???inp_a", "???inp_b"]:
        return
    if id not in clients_seen and id not in ["a","b"]: # Ensures it doesn't take inputs as an id
        player.name = id
        return id
    return False

def send_stop_signal():
    for i in range(30):
        radio.send("stop")

def waiting():
    framelist = [
        "00000:00000:00000:00000:00000",
        "00000:00000:09000:00000:00000",
        "00000:00000:09900:00000:00000",
        "00000:00000:09990:00000:00000"
    ]
    for i in framelist:
        display.show(Image(i))
        time.sleep(0.2)

while True:
    # radio.send("test") # debugging purposes
    waiting()
    detail = radio.receive_full() # receives id from nearby microbit
    if detail:
        playerid = player_checker(detail)
        if playerid:
            for i in range(60):
                radio.send(playerid+"_playsnake")
                time.sleep(0.01)
            gameloop()
