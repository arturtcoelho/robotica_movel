
import math

def gen_rot(ini, end):
    u = 2 # degrees
    return "r", int(math.degrees(math.atan((end[1]-ini[1])/(end[0]-ini[0]))) / u)

def update_rot(a, b):
    return (a[0], a[1], b[2])

def gen_lin(ini, end):
    print(ini, end)
    return "l", int(math.sqrt((end[0]-ini[0])**2 + (end[1]-ini[1])**2))

def genmov(positions):

    ua = 10 # blocks coordinates

    positions = [[(p[0]+1)*ua-ua/2, (p[1]+1)*ua-ua/2, p[2]] for p in positions]

    ur = 2
    ul = 0.5

    movs = []

    for i in range(len(positions)-1):
        pos0 = positions[i]
        pos1 = positions[i+1]

        movs += [gen_rot(pos0, pos1)]
        pos0[2] = movs[-1][1] * ur
        movs += [gen_lin(pos0, pos1)]

    return movs

if __name__ == "__main__":
    print(genmov([[0, 0, 0], [4, 6, 90], [6, 8, 0]]))