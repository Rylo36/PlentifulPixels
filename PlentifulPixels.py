from graphics import *
import math
import random

#Config
windowsize = 1000 #window dimensions, recommended is 1000
resolution = 10 #size of a pixel, recommended is 10
#WARNING: The resolution CAN NOT be higher than the window size

pixeloff = "black"

#Graphics Engine
nec = windowsize / resolution
pixel = []
enablesquare = True
enablecircle = True
colorsupport = True

#Physics Engine
objects = []
raw = []
enablecollision = False

win = GraphWin("Plentiful Pixels by Ryan Lopez", windowsize, windowsize)

#Objects

class Object:
    type = "None" #Square, Circle, or None
    color = 1#Color of object, can be 1-5 depending on wanted color anything above 5 is white
    x = 0
    y = 0
    vx = 0
    vy = 0
    size = 20#This will never change (unless done here)


def main():
    #Setup

    CreatePixels()
    CreateRandomObject()


    while True:
        #Physics()
        Render()

def CreateRandomObject():
    global object

    cur = len(objects)

    objects.append(Object())

    objects[cur].type = "Square"
    objects[cur].x = random.randint(1,windowsize)
    objects[cur].y = random.randint(1,windowsize)
    objects[cur].vx = random.randint(-2,2)
    objects[cur].vy = random.randint(-2,2)
    objects[cur].color = random.randint(1,4)
    
def CreatePixels():
    global pixel
    global raw
    a = 0
    b = 0
    c = 0
    d = 0
    slot = 0

    while(a < nec):
        while(b < nec):
            pixel.append(Rectangle(Point(d - resolution,c - resolution),Point(d + resolution,c + resolution)))
            pixel[slot].draw(win)
            slot += 1
            b += 1
            d += resolution

        
        a += 1
        c += resolution

def ClearRender():
    global pixel

    #Notice how the pixel is NOT undrawn before it is deleted. Doing so would cause the window to flash every frame update
    a = len(pixel) - 1
    while(a > 1):
        pixel[a].undraw()
        del pixel[a]
        a -= 1

def Render():
    global pixel
    global raw

    a = 0
    b = 0
    c = 0
    d = 0
    slot = 0

    while(a < nec):
        c += resolution
        while(b < nec):
            d += resolution
            rgb = round(Blend(c,d))
            if(rgb == 0):
                pixel[slot].setFill(pixeloff)
            if(rgb == 1):
                pixel[slot].setFill("red")
            if(rgb == 2):
                pixel[slot].setFill("blue")
            if(rgb == 3):
                pixel[slot].setFill("green")
            if(rgb == 4):
                pixel[slot].setFill("yellow")
            if(rgb >= 5):
                pixel[slot].setFill("white")
            slot += 1
            b += 1
        d = 0
        a += 1

def Present(x = 0,y = 0,cur = 1):
    global objects

    size = objects[cur].size
    ox = objects[cur].x
    oy = objects[cur].y

    if(objects[cur].type == "Square"):
        if(x < ox + size and x > ox - size and y < oy + size and oy > oy - size):
            return True
        else:
            return False
    elif(objects[cur].type == "None" or objects[cur] == None):
        return False

def Blend(x = 0, y = 0):
    global objects
    color = 0
    cur = 0
    while(cur < len(objects)):
        if(Present(x,y,cur) == True):
            color += objects[cur].color
        cur += 1
            
    return color


main()
