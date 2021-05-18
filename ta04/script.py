import math
from math import sin, cos

import tkinter as tk

from threading import Thread
from time import sleep

base_x = 30
base_y = 30

field_side = 100
field_division = 10

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
        self.y = -int(bot[1]) + field_side -self.side/2
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

    def print_bot(self, pos):
        bot_square = Square(pos)
        self.canvas.create_polygon(self.coord(bot_square.square_back), fill="orange", outline="black")
        self.canvas.create_polygon(self.coord(bot_square.square_front), fill="red", outline="black")

    def update(self, pos):
        self.canvas.delete("all") # delete the old polygon

        self.print_field()
        self.print_bot(pos)

        self.root.update()

    def callback(self):
        self.root.quit()

    def run(self):
        try:
            self.root.mainloop()
        except AttributeError:
            pass

wheel_radius = 3
wheel_circunference = 2*math.pi*wheel_radius
wheel_axis = 30

fraction_spin = wheel_circunference / 36
full_spin = wheel_circunference

max_speed = 15 # rpm
max_speed = max_speed / 60 # rps
max_speed = max_speed * 360 # degrees/s

stop_speed = 0 # rpm

def vec_dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) 

def gen_linear(initial, end):
    p = initial
    a = math.radians(initial[2])
    k = 0.25
    i = 0
    lim = 200
    l = [p]
    while (vec_dist(p, end) > k*1.5 and i < lim):
        p = (p[0] + k*math.cos(a), p[1] + k*math.sin(a), initial[2])
        i += 1
        l += [p]
    return l + [end]

def gen_rot(initial, end):
    p = initial
    a = math.radians(initial[2])
    k = 2
    i = 0
    lim = 180
    l = [p]
    while (math.fabs(p[2]-end[2]) > k*1.5 and i < lim):
        p = (p[0], p[1], p[2] + (2*k if p[2] < end[2] else -2*k))
        i += 1
        l += [p]
    return l + [end]

# (x, y, angle)
positions = gen_rot((0, 0, 0), (0, 0, 56.31)) + \
            gen_linear((0, 0, 56.31), (4, 6, 56.31)) + \
            gen_rot((4, 6, 56.31), (4, 6, 90)) + \
            gen_rot((4, 6, 90), (4, 6, 45)) + \
            gen_linear((4, 6, 45), (6, 8, 45)) + \
            gen_rot((6, 8, 45), (6, 8, 0))

def coord_to_cm(c):
    return (c[0]*field_division+field_division/2, c[1]*field_division+field_division/2, math.radians(c[2]))

inf = Interface()    
for p in positions:
    inf.update(coord_to_cm(p))
    sleep(0.05)

input()