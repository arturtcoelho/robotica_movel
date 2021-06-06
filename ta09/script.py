import math
from math import *

import tkinter as tk

from threading import Thread
from time import sleep

from random import random

import numpy as np

base_x = 30
base_y = 30

field_side = 200
field_division = 10
num_square = field_side / field_division
side = field_division

# generate a map with a clear main diagonal
field_map = []
for i in range(int(random() * 100)//19 + 5):
    x = int(random()*num_square)
    y = int(random()*num_square)
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
        self.root.geometry("%dx%d+%d+%d" % (800,800,xcoord,ycoord))

        #set up canvas
        self.canvas = tk.Canvas(self.root, relief=tk.FLAT, background="green")
        self.canvas.pack(fill=tk.BOTH, expand=1)

    def coord(self, iterable):
        return [(item*3 + (base_y if i%2 else base_x)) 
            for i, item in enumerate(iterable)]

    def print_lines(self, lines):
        for l in lines:
            self.canvas.create_line(self.coord(l))

    def print_lines_2(self, lines):
        for l in lines:
            self.canvas.create_line(self.coord(l), fill="red")

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

    def print_bot(self, pos):
        bot_square = Square(pos)
        self.canvas.create_polygon(self.coord(bot_square.square_back), fill="orange", outline="black")
        self.canvas.create_polygon(self.coord(bot_square.square_front), fill="red", outline="black")

    def print_bot_2(self, pos):
        bot_square = Square(pos)
        self.canvas.create_polygon(self.coord(bot_square.square_back), fill="pink", outline="black")
        self.canvas.create_polygon(self.coord(bot_square.square_front), fill="purple", outline="black")

    def print_measures(self, lines):
        self.print_lines(lines)   
    
    def print_measures_2(self, lines):
        self.print_lines_2(lines)

    def update(self, pos, lines, pos2, lines2):
        self.canvas.delete("all") # delete the old polygon

        self.print_field()
        self.print_map()
        self.print_measures(lines)
        self.print_bot(pos)
        if (pos2):
            self.print_bot_2(pos2)
        if (lines2):
            self.print_measures_2(lines2)

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

def convert_angle(a):
    if (a > 3*pi/2):
        return 2*pi - a
    return a

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

# bot pose
bot = [int(random()*10)*num_square, 
        int(random()*10)*num_square, 
        radians(int(random()*24)*15)]

err = np.random.normal(1, 0.01, len(field_map)*2)

# map (points) converted and map with deviation
field_map_c = [[p[0]*10+5, p[1]*10+5] for p in field_map]
field_map_dev = [[p[0]*err[i], p[1]*err[i*2]] 
                    for i, p in enumerate(field_map_c)]

# perfect measures and deviated measures (distance, angle)
measurements = [[vec_dist(p, bot), -atan2(p[1] - bot[1], p[0] - bot[0])] 
                for p in field_map_c]
m_dev = [[vec_dist(p, bot), -atan2(p[1] - bot[1], p[0] - bot[0]), p[0], p[1]] 
                for p in field_map_dev]

# pairs bot/point and deviated pairs
m_pairs = [[p[0], p[1], bot[0], bot[1]] for p in field_map_c]
# only if in front of bot
m_pairs_dev = [[p[0], p[1], bot[0], bot[1]] for p in field_map_dev 
        if -pi/2 <= 
            math.fmod(convert_angle(bot[2] + atan2(p[1] - bot[1], p[0] - bot[0])), radians(360)) 
        <= pi/2]
m_pairs_dev_full = [[p[0], p[1], bot[0], bot[1]] for p in field_map_dev]

# measures (distance, angle) converted to bot pov
# only if in front of bot
m_bot = [[m[0], math.fmod(convert_angle(bot[2] - m[1]), radians(360)), m[2], m[3]] for m in m_dev 
        if -pi/2 <= math.fmod(convert_angle(bot[2] - m[1]), radians(360)) <= pi/2]

print([bot[0], bot[1], math.degrees(bot[2])])
print([[m[0], math.degrees(m[1])] for m in m_bot])

# Initialize tkinter
inf = Interface()
inf.update(bot, m_pairs_dev, None, None)

if (len(m_bot) < 3):
    print("not enough measurements")
    exit()

# calculate position
# original map == field_map_c
# measurements == m_bot[distance, angle, x, y]

# get all the distances
z0 = m_bot[0]
zi = m_bot[1]
zj = m_bot[2]

# calculate the right side of the linear system
A = ((z0[0]**2- zi[0]**2 - z0[2]**2 + zi[2]**2 - z0[3]**2 + zi[3]**2))/2
B = ((z0[0]**2- zj[0]**2 - z0[2]**2 + zj[2]**2 - z0[3]**2 + zj[3]**2))/2

# calculate the coefficients of Px and Py
a = (zi[2] - z0[2])
b = (zi[3] - z0[3])
c = (zj[2] - z0[2])
d = (zj[3] - z0[3])

# calculate Px and Py
yr = (B*a - A*c)/(a*d - b*c)
xr = (A/a) - ((b/a)*yr)

bot2 = [xr, yr, bot[2]]

print(bot2)

inf.update(bot, m_pairs_dev, bot2, m_pairs_dev[0:3])

input()