from graphics import *
import math
import random

#Config
windowsize = 600 #window dimensions, recommended is 1000
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

#Object Maker Timer

timer = [0,20] #Do not touch timer[0]

#Objects

class Object:
    type = "None" #Square, Circle, or None
    color = [0,0,0]#Color of object, can be 1-5 depending on wanted color anything above 5 is white
    x = 0
    y = 0
    vx = 0
    vy = 0
    size = 50#This will never change (unless done here)


def main():
    global timer
    #Setup

    CreatePixels()
    CreateRandomObject()
    CreateRandomObject()
    CreateRandomObject()
    CreateRandomObject()
    CreateRandomObject()

    while True:
        
        timer[0] += 1

        if(timer[0] >= timer[1]):
            timer[0] = 0
            CreateRandomObject()
        ObjectCleaner() #Removes objects that are off the screen
        Physics()
        Render()

def ObjectCleaner():
    global objects

    bounds = Object.size

    cur = len(objects) - 1
    while(cur >= 0):
        if(objects[cur].x < 0 - bounds or objects[cur].y < 0 - bounds):
            DeleteObject(cur)
        elif(objects[cur].x > windowsize + bounds or objects[cur].y > windowsize + bounds):
            DeleteObject(cur)
        cur -= 1

def DeleteObject(cur):
    global objects
    del objects[cur]

   


def Physics():
    global objects
    global enablecollision

    max = len(objects)
    a = 0

    while(a < max):
        
        if(enablecollision == False):
            objects[a].x += objects[a].vx
            objects[a].y += objects[a].vy

        a += 1

def CreateRandomObject():
    global objects

    cur = len(objects)

    objects.append(Object())

    speed = 30
    if(random.randint(1,2) == 1):
        objects[cur].type = "Circle"
    else:
        objects[cur].type = "Circle"
    objects[cur].x = random.randint(1,windowsize)
    objects[cur].y = random.randint(1,windowsize)
    objects[cur].vx = random.randint(-speed,speed)
    objects[cur].vy = random.randint(-speed,speed)
    objects[cur].color = [random.randint(1,255),random.randint(1,255),random.randint(1,255)]
    
def CreatePixels():
    global pixel
    global raw
    global nec
    global windowsize
    a = 0
    b = 0
    c = 0
    d = 0
    slot = 0

    while(c < windowsize):
        while(d < windowsize):
            pixel.append(Rectangle(Point(c,d),Point(c + resolution,d + resolution)))
            #print(c," - ",d)
            pixel[slot].draw(win)
            slot += 1
            d += resolution
            b += 1
            

        b = 0
        d = 0
        c += resolution
        a += 1
        
    print(slot, " Pixels Created!")

def ClearRender():
    global pixel

    #Notice how the pixel is NOT undrawn before it is deleted. Doing so would cause the window to flash every frame update
    a = len(pixel) - 1
    while(a > 1):
        #pixel[a].undraw()
        del pixel[a]
        a -= 1

def Render():
    global pixel
    global raw
    global nec

    a = 0
    b = 0
    c = resolution
    d = resolution
    slot = 0

    while(c < windowsize):
        while(d <= windowsize):
            
            rgb = [0,0,0]
            rgb[0] = round((Blend(c,d,0) + Blend(c - (resolution / 2),d - (resolution / 2),0) + Blend(c - resolution,d - resolution,0) + Blend(c,d - resolution,0) + Blend(c - resolution,d,0)) / 5)
            rgb[1] = round((Blend(c,d,1) + Blend(c - (resolution / 2),d - (resolution / 2),1) + Blend(c - resolution,d - resolution,1) + Blend(c,d - resolution,1) + Blend(c - resolution,d,1)) / 5)
            rgb[2] = round((Blend(c,d,2) + Blend(c - (resolution / 2),d - (resolution / 2),2) + Blend(c - resolution,d - resolution,2) + Blend(c,d - resolution,2) + Blend(c - resolution,d,2)) / 5)
            pixel[slot].setFill(color_rgb(rgb[0],rgb[1],rgb[2]))
            #if(rgb <= 0):
            #    pixel[slot].setFill(pixeloff)
            #if(rgb == 1):
            #    pixel[slot].setFill("red")
            #if(rgb == 2):
            #    pixel[slot].setFill("blue")
            #if(rgb == 3):
            #    pixel[slot].setFill("green")
            #if(rgb == 4):
            #    pixel[slot].setFill("yellow")
            #if(rgb >= 5):
            #    pixel[slot].setFill("white")
            slot += 1
            d += resolution
            b += 1
        b = 0
        d = 0
        c += resolution
        a += 1

def Present(x = 0,y = 0,cur = 1):
    global objects

    size = objects[cur].size
    ox = objects[cur].x
    oy = objects[cur].y
    r = resolution
    pi = math.pi
    distance = math.sqrt(((abs(ox -x)*(abs(ox -x)) + (abs(oy - y)) * (abs(oy - y)))))

    if(objects[cur].type == "Square"):
        if(x <= ox + size and x >= ox - size and y <= oy + size and y >= oy - size):
            return True
        else:
            return False
    elif(objects[cur].type == "Circle"):
        if(distance <= size):
            return True
        else:
            return False
    elif(objects[cur].type == "None" or objects[cur] == None):
        return False

def Blend(x = 0, y = 0,mode = 0):
    global objects
    color = 0
    cur = 0
    while(cur < len(objects)):
        if(Present(x,y,cur) == True):
            if(color == 0):
                color = objects[cur].color[mode]
            else:
                color = (objects[cur].color[mode] + color[mode]) / 2
        cur += 1
            
    return color


main()
