from microbit import *
import time


def clear_map():
    global ledmap
    ledmap = [
        [ 0,0,0,0,0 ],
        [ 0,0,0,0,0 ],
        [ 0,0,0,0,0 ],
        [ 0,0,0,0,0 ],
        [ 0,0,0,0,0 ]
    ]

class Snake:
    def __init__(self):
        self.body_dict = { # dy, dx
            "piece_1": [0,0]
        } # Holds the pieces of the body and the coordinates of each on the ledmap
        #self.direction = "right"
        self.direction = ["right","down","left","up"] # index 0 is the current direction
       # self.prev_location = # previous location of last piece

    def change_direction(self, button):
        if button == "a":
            self.direction = [self.direction[1],self.direction[2],self.direction[3],self.direction[0]]
        else:
            self.direction = [self.direction[3],self.direction[0],self.direction[1],self.direction[2]]
    def move(self): # Reverse iteration through self.body_dict. every piece takes the coordinates of the one above them in the body, and piece_1 moves according to direction
        #lets start off with piece 1 moving only
        dy_dx = {
            "right": [0,1],
            "left": [0,-1],
            "up": [-1,0],
            "down": [1,0]
        }[self.direction[0]]
        self.body_dict["piece_1"][0] += dy_dx[0] #dy
        self.body_dict["piece_1"][1] += dy_dx[1] #dx

    def extend_body(self):
        self.body_dict["piece_{0}".format(len(self.body_dict)+1)]

player = Snake()

while True: # Game loop
    clear_map()
    time.sleep(0.5)
    if button_a.is_pressed():
        player.change_direction("a")
    elif button_b.is_pressed():
        player.change_direction("b")
    for piece in player.body_dict:
        ledmap[player.body_dict[piece][0]][player.body_dict[piece][1]] = 5
    player.move()
    imgstring = ":".join("".join(str(item) for item in ledlist) for ledlist in ledmap)
    output = Image(imgstring)
    
    display.show(output)
