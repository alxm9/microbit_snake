from microbit import *
import music
import time
import speech
import random

class Snake:
    def __init__(self):
        self.body_dict = { # y, x
            "piece_1": [0,0] # Starting off with one piece only
        #   "piece_2": [0,0]
        #   "piece_....
        } # Holds the pieces of the body and the coordinates of each on the ledmap
        #self.direction = "right"
        self.direction = ["right","down","left","up"] # index 0 is the current direction
        self.alive = True
       # self.prev_location = # previous location of last piece

    def change_direction(self, button):
        if button == "b": # clockwise
            self.direction = [self.direction[1],self.direction[2],self.direction[3],self.direction[0]]
        else: # counter-clockwise
            self.direction = [self.direction[3],self.direction[0],self.direction[1],self.direction[2]]
    def move(self): # Reverse iteration through self.body_dict. every piece takes the coordinates of the one above them in the body, and piece_1 moves according to direction
        #lets start off with piece 1 moving only
        global time_interval

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
                time_interval = time_interval * 0.9 # speeds up game
                speech.say("chomp")
                fruit.change_location()

        # location of every piece replaced with its "parent". piece_5 to piece_4, piece_4 to piece_3...
        for number in range(len(self.body_dict),1,-1):
            self.body_dict["piece_{0}".format(number)][0] = self.body_dict["piece_{0}".format(number-1)][0]
            self.body_dict["piece_{0}".format(number)][1] = self.body_dict["piece_{0}".format(number-1)][1]
        self.body_dict["piece_1"][0] += dy_dx[0] #dy 
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

def clear_map():
    global ledmap
    ledmap = [
        [ 0,0,0,0,0 ],
        [ 0,0,0,0,0 ],
        [ 0,0,0,0,0 ],
        [ 0,0,0,0,0 ],
        [ 0,0,0,0,0 ]
    ]

def check_input(player):
    if button_a.was_pressed(): 
        player.change_direction("a")
    elif button_b.was_pressed():
        player.change_direction("b")

def refresh_display(): # Converts the ledmap into a string that can be passed to display.show. String looks something like 00000:00000:00000:00000:00000
    for piece in player.body_dict: #
        ledmap[player.body_dict[piece][0]][player.body_dict[piece][1]] = 9
    ledmap[fruit.location[0]][fruit.location[1]] = 9
    imgstring = ":".join("".join(str(item) for item in ledlist) for ledlist in ledmap)
    output = Image(imgstring)
    
    display.show(output)

player = Snake()
fruit = Edible()
time_interval = 0.5

while player.alive: # Game loop
    clear_map()
    check_input(player)
    time.sleep(time_interval)
    check_input(player) # checking inputs immediately before and after time.sleep seems to have better effect on the input
    player.move()
    refresh_display()

final_score = str(len(player.body_dict))
speech.say("game ouver") #misspelt on purpose as its easier to make out the audio output. Kinda like the NATO phonetic alphabet.
time.sleep(0.3)
display.show(Image.SAD)
speech.say("final score is")
speech.say(final_score)