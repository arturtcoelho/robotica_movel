import math
from math import *

import tkinter as tk

from threading import Thread
from time import sleep

from random import random

base_x = 30
base_y = 30

field_side = 100
field_division = 10
side = field_division

# generate a map with a clear main diagonal
field_map = []
for i in range(40):
    x = int(random() * 10)
    y = int(random() * 10)
    while (x in range(y-2, y+2)):
        x = int(random() * 10)
    field_map.append([x, y])

def convert_sq(sq):
    sq = [sq[0] * side, sq[1] * side]
    return [sq[0], sq[1], 
            sq[0] + side, sq[1], 
            sq[0] + side, sq[1] + side, 
            sq[0], sq[1] + side]

class Square():

    side = 10
    half = side / 2
    square_back = [ 
        0,0,
        half,0, 
        half,side, 
        0,side
    ]
    square_front = [ 
        half,0,
        side,0, 
        side,side, 
        half,side
    ]

    def __init__(self, bot):
        self.x = int(bot[0]) - self.side/2
        self.y = int(bot[1]) - self.side/2
        self.angle = -bot[2]
        self.square_back = [ self.square_back[i] + (self.y if i % 2 else self.x) for i in range(8)]
        self.square_front = [ self.square_front[i] + (self.y if i % 2 else self.x) for i in range(8)]
        self.rotate_front(self.angle)
        self.rotate_back(self.angle)

    def rotate_front(self, angle):
        for i in range(0, 8, 2):
            s = sin(angle)
            c = cos(angle)
            x0 = self.square_front[i] - self.x - self.side/2
            y0 = self.square_front[i+1] - self.y - self.side/2

            x_new = x0 * c - y0 * s
            y_new = x0 * s + y0 * c

            self.square_front[i] = x_new + self.x + self.side/2
            self.square_front[i+1] = y_new + self.y + self.side/2

    def rotate_back(self, angle):
        for i in range(0, 8, 2):
            s = sin(angle)
            c = cos(angle)
            x0 = self.square_back[i] - self.x - self.side/2
            y0 = self.square_back[i+1] - self.y - self.side/2

            x_new = x0 * c - y0 * s
            y_new = x0 * s + y0 * c

            self.square_back[i] = x_new + self.x + self.side/2
            self.square_back[i+1] = y_new + self.y + self.side/2

class Interface(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()

        self.root = tk.Tk()

        # set window to middle of screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        xcoord = screen_width//2
        ycoord = screen_height//2 - 300
        self.root.geometry("%dx%d+%d+%d" % (600,600,xcoord,ycoord))

        #set up canvas
        self.canvas = tk.Canvas(self.root, relief=tk.FLAT, background="green")
        self.canvas.pack(fill=tk.BOTH, expand=1)

    def coord(self, iterable):
        return [(item*5 + (base_y if i%2 else base_x)) 
            for i, item in enumerate(iterable)]

    def print_lines(self, lines):
        for l in lines:
            self.canvas.create_line(self.coord(l))

    def print_field(self):
        l = []

        for i in range(int(field_side/field_division)+1):
            l+=[[0, field_division*i, field_side, field_division*i]]

        for i in range(int(field_side/field_division)+1):
            l+=[[field_division*i, 0, field_division*i, field_side]]

        self.print_lines(l)

    def print_map(self):
        for sq in field_map:
            self.canvas.create_polygon(self.coord(convert_sq(sq)), fill="blue", outline="black")

    def print_found_map(self, m):
        if m == []: return
        for sq in m:
            self.canvas.create_polygon(self.coord(convert_sq(sq)), fill="lightblue", outline="black")

    def print_bot(self, pos):
        bot_square = Square(pos)
        self.canvas.create_polygon(self.coord(bot_square.square_back), fill="orange", outline="black")
        self.canvas.create_polygon(self.coord(bot_square.square_front), fill="red", outline="black")

    def update(self, pos, m):
        self.canvas.delete("all") # delete the old polygon

        self.print_field()
        self.print_map()
        self.print_found_map(m)
        self.print_bot(pos)


        self.root.update()

    def callback(self):
        self.root.quit()

    def run(self):
        try:
            self.root.mainloop()
        except AttributeError:
            pass

def vec_dist(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# dummy function to add global know map to our 'found' map based on proximity
def fill_map(x, y, m):
    x = x/10
    y = y/10
    dist = 2.5
    found = []
    for sq in m:
        if (vec_dist([x, y], sq) < dist):
            found += [sq]

    return found


# Entry point
# Initialize tkinter
inf = Interface()   
inf.update([0, 0, radians(-45)], []) 

# list of found points
our_map = []
for i in range(100):

    # find points in coordinates
    our_map += fill_map(i, i, field_map)

    # Update tkinter map
    inf.update([i, i, radians(-45)], our_map)
    sleep(0.1)

input()