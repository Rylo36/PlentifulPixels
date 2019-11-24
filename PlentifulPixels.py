from graphics import *
import math
import random

#Config
windowsize = 500 #window dimensions, recommended is 500
resolution = 20 #size of a pixel, recommended is 20
objectstohave = 8#Number of objects to have on the canvas at all times
#WARNING: The resolution CAN NOT be higher than the window size

pixeloff = "black"

#Graphics Engine
nec = windowsize / resolution
pixel = []
enablesquare = True
enablecircle = True
colorsupport = True

#Color Config
maxintensity = 200
minintensity = 100
deepeffect = 2 #Only change this if you know what your doing, i recommend 2

#Physics Engine
objects = []
raw = []
enablecollision = False

#Performance
fasterplease = False #Set it to true if you experience slow render times
lowres = False #Set it to true if you must, but i really recommend the hd colors if you can

win = GraphWin("Plentiful Pixels by Ryan Lopez", windowsize, windowsize)

#Object Maker Timer

timer = [-1,10] #Do not touch timer[0]

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
    global objectstohave
    global objects
    #Setup

    CreatePixels()

    a = 0

    while(a < objectstohave):
        CreateRandomObject()
        a += 1

    while True:
        #if(timer[0] != -1):
        #    timer[0] += 1

        #    if(timer[0] >= timer[1]):
        #        timer[0] = 0
        #        CreateRandomObject()

        if(len(objects) < objectstohave):
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
    global maxintensity
    global minintensity

    cur = len(objects)

    objects.append(Object())

    speed = 30
    if(random.randint(1,2) == 1):
        objects[cur].type = "Square"
    else:
        objects[cur].type = "Circle"
    objects[cur].x = random.randint(1,windowsize)
    objects[cur].y = random.randint(1,windowsize)
    objects[cur].vx = random.randint(-speed,speed)
    objects[cur].vy = random.randint(-speed,speed)
    objects[cur].color = [random.randint(minintensity,maxintensity),random.randint(minintensity,maxintensity),random.randint(minintensity,maxintensity)]
    
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
        while(d <= windowsize):
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
    c = 0
    d = 0
    slot = 0

    while(c < windowsize):
        while(d <= windowsize):
            
            rgb = [0,0,0]
            if(fasterplease == False):
                rgb[0] = round((Blend(c,d,0) + Blend(c - (resolution / 2),d - (resolution / 2),0) + Blend(c - resolution,d - resolution,0) + Blend(c,d - resolution,0) + Blend(c - resolution,d,0)) / 5)
                rgb[1] = round((Blend(c,d,1) + Blend(c - (resolution / 2),d - (resolution / 2),1) + Blend(c - resolution,d - resolution,1) + Blend(c,d - resolution,1) + Blend(c - resolution,d,1)) / 5)
                rgb[2] = round((Blend(c,d,2) + Blend(c - (resolution / 2),d - (resolution / 2),2) + Blend(c - resolution,d - resolution,2) + Blend(c,d - resolution,2) + Blend(c - resolution,d,2)) / 5)
            else:
                rgb[0] = round(Blend(c,d,0))
                rgb[1] = round(Blend(c,d,1))
                rgb[2] = round(Blend(c,d,2))
            
            if(colorsupport == False):
                rgb[1] = rgb[0]
                rgb[2] = rgb[0]

            pixel[slot].setFill(color_rgb(rgb[0],rgb[1],rgb[2]))
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

    if(objects[cur].type == "Square" and enablesquare == True):
        if(x <= ox + size and x >= ox - size and y <= oy + size and y >= oy - size):
            return True
        else:
            return False
    elif(objects[cur].type == "Circle" and enablecircle == True):
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

            
            postdeep = 0
            if(lowres == False):
                distance = math.sqrt(((abs(objects[cur].x -x)*(abs(objects[cur].x -x)) + (abs(objects[cur].y - y)) * (abs(objects[cur].y - y)))))
                postdeep = objects[cur].color[mode] - (distance * deepeffect)

                if(postdeep < 0):
                    postdeep = 0

                round(postdeep)
            else:
                postdeep = objects[cur].color[mode]

            if(color == 0):
                color = postdeep
            else:
                color = (postdeep + color) / 2
        cur += 1
            
    return color


main()
