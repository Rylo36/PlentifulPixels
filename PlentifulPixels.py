from graphics import *
import math
import random

#Config <START OF CONFIG> --------------------------------------------------------------------
allowphysics = True #Disable physics if you would like by setting it to false
enableobjectmaker = False #Allows the user to create objects manually 
automakeobjects = True #Randomly Generate Objects, will not exceed the object max #
windowsize = 500 #window dimensions, recommended is 500
resolution = 15 #size of a pixel, recommended is 20
objectstohave = 10#Number of objects to have on the canvas at all times
#WARNING: The resolution CAN NOT be higher than the window size

#Background
pixeloff = "black"

#Graphics Engine
enablesquare = True #Who doesn't like Squares?
enablecircle = True
colorsupport = True #No real practical use, everyone likes color

#Color Config
maxintensity = 250 #max rgb value
minintensity = 100 #min rgb value
deepeffect = 2 #This changes how quickly an object changes in opacity (the higher, the quicker), I recommend 2

#Physics Engine

enablecollision = False #Not currently working (planned to be)

#Objects

minsize = 30
maxsize = 50

#Performance
fasterplease = False #Set it to true if you experience slow render times
lowres = False #Set it to true if you must, but i really recommend the hd colors if you can

# Keybinds:
# s = decrease the size of objects created through the create tool
# s + shift = increase the size of objects created through the create tool
# z = undo (currently it can only go back one step)
# esc = delete all objects
# p = toggle physics
# t = toggle between shapes
# r = toggle random generation of shapes


#Begin Setup <END OF CONFIG> ----------------------------------------------------------------------------------

objects = []
raw = []
nec = windowsize / resolution  #Please dont touch
pixel = []

win = GraphWin("Plentiful Pixels by Ryan Lopez", windowsize, windowsize)

notify = Text(Point(windowsize / 2, windowsize / 20), "Someone forgot to add text")
notifytimer = [-1,120]
notify.setSize(30)

notifymore = Text(Point(windowsize / 2, windowsize / 10), "Someone forgot to add data")
notifymore.setSize(15)
notify.setFill("white")

#Object Maker Timer, please ignore
lastplaced = -1
timer = [0,10] #Do not touch timer[0]



class Object:
    type = "None" #Square, Circle, or None
    color = [0,0,0]#Color of object, can be 1-5 depending on wanted color anything above 5 is white
    x = 0
    y = 0
    vx = 0
    vy = 0
    rot = 0 #AKA Rotation
    size = 50#This will never change (unless done here)

class Tool:
    type = "Square"
    size = 50
    color = [0,0,0]
    vx = 0
    vy = 0

undocounter = 0
tool = Tool()
toollog = []

def leftclick(event):
    global toollog
    global tool
    global lastplaced
    toollog.append(len(objects))
    CreateObject(event.x,event.y,tool.size,tool.type)

def rightclick(event):
    global lastplaced
    if(lastplaced == -1):
        print("Leftclick does nothing at all")
    else:
        objects[lastplaced].color = [objects[lastplaced].color[0] ]

def realtime():
    global notify
    global notifymore
    global tool
    global notifytimer
    global allowphysics
    global win
    global objectstohave
    global objects
    global lastplaced
    global automakeobjects
    global toollog
    global undocounter

    if(notifytimer[0] < -1):
        notifytimer[0] = -1
    elif(notifytimer[0] == 0):
        notifytimer[0] = -1
        notify.undraw()
        notifymore.undraw()
    elif(notifytimer[0] > 0):
        notifytimer[0] -= 1

    checkString = win.checkKey()
    if(checkString != None):
        if(checkString == "Escape"): 
            objects = []
            toollog = []
            Notify("Objects Cleared"," ","yellow")
        if(checkString == "p"): 
            if(allowphysics == True): 
                allowphysics = False
                Notify("Physics Disabled","Press p to renable","red")
            else: 
                allowphysics = True
                Notify("Physics Enabled","Press p to disable","green")
        if(checkString == "r"): 
            if(automakeobjects == True): 
                automakeobjects = False
                Notify("Shape Generation Disabled","Press r to renable","red")
            else: 
                automakeobjects = True
                Notify("Shape Generation Enabled","Press r to disable","green")
        if(checkString == "s"):
                tool.size += 10
                Notify("Size Increased",tool.size,"green")
        if(checkString == "S"):
                tool.size -= 10
                Notify("Size Decreased",tool.size,"red")
        if(checkString == "z"):
                if(len(toollog) > 0):
                    undocounter += 1
                    Notify("Actions Undone:",undocounter,"yellow")
                else:
                    Notify("Error","No Actions to Undo","red")
        if(checkString == "t"):
                if(tool.type == "Square"):
                    tool.type = "Circle"
                    Notify("Shape Selected:",tool.type,"yellow")
                else: 
                    tool.type = "Square"
                    Notify("Shape Selected:",tool.type,"yellow")

        if(undocounter > len(toollog) -1): undocounter = len(toollog) - 1
            

def main():
    global notify
    global notifymore
    global tool
    global notifytimer
    global allowphysics
    global win
    global objectstohave
    global objects
    global undocounter
    global toollog
    #Setup
    win.bind('<Button-1>', leftclick)
    win.bind('<Button-3>', rightclick)

    CreatePixels()

    a = 0

    while(a < objectstohave):
        CreateObject()
        a += 1

    while True:
        #if(timer[0] != -1):
        #    timer[0] += 1

        #    if(timer[0] >= timer[1]):
        #        timer[0] = 0
        #        CreateObject()

        if(len(objects) < objectstohave and automakeobjects == True):
            CreateObject()


        if(undocounter > len(toollog) -1): undocounter = len(toollog) - 1

        while(undocounter > 0):
            a = len(toollog) - 1
            DeleteObject(toollog[a])
            del toollog[a]
            undocounter -= 1
            
                    
        
        ObjectCleaner() #Removes objects that are off the screen
        if(allowphysics == True): Physics()
        Render()

def Notify(msg = "None",submsg = "none", color = "white", time = -1):
    global notify
    global notifymore
    global win
    global notifytimer
    notifymore.setText(submsg)
    notify.setTextColor(color)
    notify.setText(msg)
    notifymore.setTextColor(color)
    if(notifytimer[0] == -1):
        notify.draw(win)
        notifymore.draw(win)
    if(time == -1): notifytimer[0] = notifytimer[1]
    else: notifytimer = time


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
    global toollog
    del objects[cur]
    
    a = len(toollog)
    while(a > 0):
        if(toollog[a] == cur):
            del toollog[a]
        a -= 1

   


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

def CreateObject(x = random.randint(1,windowsize),y = random.randint(1,windowsize),size = random.randint(minsize,maxsize),type = "Random"):
    global objects
    global maxintensity
    global minintensity
    
    cur = len(objects)

    objects.append(Object())

    speed = 60
    if(type == "Random"):
        if(random.randint(1,2) == 1):
            objects[cur].type = "Square"
        else:
            objects[cur].type = "Circle"
    else: objects[cur].type = type
    objects[cur].size = size
    objects[cur].x = x
    objects[cur].y = y
    objects[cur].vx = random.randint(-speed,speed)
    objects[cur].vy = random.randint(-speed,speed)
    if(objects[cur].vx == 0):
        objects[cur].vx = 10
    if(objects[cur].vy == 0):
        objects[cur].vy = 10
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

            realtime()
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
