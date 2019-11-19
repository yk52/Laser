#!/usr/bin/env python
"""
19/11/19
Take the path entered into the laser GUI and convert it into a visual basic script (.vbs) script
"""

import os
import math
#import pyximport; pyximport.install()

unit = 1.0    # smallest unit = 1 micrometer

# global user variables
fileName = ""
startX = 0
startY = 0
startZ = 0
startLeistung = 0
pulse = 0
repRate = 0
numShots = 0
pulseEnergy = 0
hv = 0
energyMode = 0
triggerMode = 0
waitMs = 0
rasterfahrt = 0
pitch = 1   # TODO change back to 0 later

	
"""
Sets global parameters from GUI input for all functions to use
"""
def setParams(array):
    # Maybe it was a mistake to use global variables.........
    global fileName
    global startX 
    global startY
    global startZ
    global startLeistung
    global pulse
    global repRate
    global puseEnergy
    global hv
    global energyMode
    global triggerMode
    global waitMs
    global pitch

    i = 0
    fileName = array[i]   # Name of file to be saved as
    i += 1
    startX = array[i]   # x Coordinate
    i += 1
    startY = array[i]   # y Coordinate
    i += 1
    startZ = array[i]   # z Coordinate
    i += 1
    startLeistung = array[i]    # Attenuator position in degrees
    i += 1
    pulse = array[i]    # Number of pulses before laser is shot
    i += 1
    repRate = array[i]  # Pulse duration = 1us / repRate
    i += 1
    pulseEnergy = array[i]
    i += 1
    hv = array[i]
    i += 1
    energyMode = array[i]
    i += 1
    triggerMode = array[i]
    i += 1
    waitMs = array[i]   # wait for x ms after waituntilinpos 
    i += 1
    pitch = array[i]
	
def defineVars(f):
    global startX 
    global startY
    global startZ
    global startLeistung
    global pulse
    global puseEnergy
    global hv
    global energyMode
    global triggerMode
    global waitMs

    f.write("' Define all used variables ***************************************************\n\n")
    f.write("dim startX, startY, startZ, startLeistung\n")
    f.write("dim pulse\n")
    f.write("dim i,j\n")
    f.write("dim pulseEnergyDist, HVVal, energyModeVal, triggerModeVal\n")
    f.write("dim waitMs\n\n")
    f.write("startX = %.3f\n" %startX)
    f.write("startY = %.3f\n" %startY)
    f.write("startZ = %.3f\n" %startZ)
    f.write("startLeistung = %.3f\n" %startLeistung)
    f.write("pulse = %d\n" %pulse)
    f.write("pulseEnergyDist = %d\n" %pulseEnergy)
    f.write("HVVal = %d\n" %hv)
    f.write("energyModeVal = %d\n" %energyMode)
    f.write("triggerModeVal = %d\n" %triggerMode)
    f.write("waitMs = %d\n\n" %waitMs)
	
def shoot(f):
    global repRate
    f.write("PSOPulse pulse, 1000000/%f\n" %repRate)
    

"""
Move a relative distance in x and y
"""
def moveRel(f, xDist, yDist):
    f.write("\nmoveRel x, %f\n" %xDist)
    f.write("moveRel y, %f\n" %yDist)
    f.write("waituntilinpos x,y\n")
    f.write("wait waitMs\n")

"""
Move absolute distance in x and y
"""
def moveAbs(f, xPos, yPos):
    f.write("\nmove x, %f\n" %xPos)
    f.write("move y, %f\n" %yPos)
    f.write("waituntilinpos x,y\n")
    f.write("wait waitMs\n")

"""
Shoot once.
"""
def shoot(f):
    global repRate
    f.write("PSOPulse pulse, 1000000/%f\n" %repRate)


"""
Move a relative distance in x and y and shoot once
"""
def moveAndShootRel(f, xDist, yDist):
    moveRel(f, xDist, yDist)
    shoot(f)
	
"""
Move absolute distance in x and y and shoot once
"""
def moveAndShootAbs(f, x, y):
    moveAbs(f, x, y)
    shoot(f)
        

"""
move into certain direction. 0=up, 1=right, 2=down, 3=left
down and right: +
up and left: -
"""
def moveDir(f, direction, dist):
    if direction == 0:      # up
        moveRel(f, 0, -1*dist)
    elif direction == 1:      # right
        moveRel(f, dist, 0)
    elif direction == 2:      # down
        moveRel(f, 0, dist)
    elif direction == 3:      # left
        moveRel(f, -1*dist, 0)
	


"""
Move along a 2D (possibly diagonal) line and shoot in a certain pitch
"""
# TODO: what if stepX and stepY too small for movement of laser? Continue!
# Lieber mit distanz arbeiten
def twoDShoot(f, x0, x1, y0, y1):
    global pitch
    # Starting position not shot automatically
    deltaX = float(x1 - x0)
    deltaY = float(y1 - y0)
    dist = math.sqrt(pow(deltaX,2)+pow(deltaY,2))
    numShots = int(dist / float(pitch))
    stepX = deltaX / numShots
    stepY = deltaY / numShots

    x = x0
    y = y0
    xGoal = 0
    yGoal = 0

    for i in range(numShots):
        x += stepX
        y += stepY

        if (stepX > 0):
            xGoal = math.ceil(x)
        else:
            xGoal = math.floor(x)
        if (stepY > 0):
            yGoal = math.ceil(y)
        else:
            yGoal = math.floor(y)
        
        if ((yGoal >= y) or (xGoal >= x)):
            continue

        moveAndShootAbs(f, xGoal, yGoal)
	

"""
Move along a horizontal or vertical line and shoot in a certain pitch
"""
def lineRelShoot(f, direction, dist):
    # Starting position not shot automatically
    # 0 = start, 1 = stop
    global pitch
    numShots = int(dist / pitch)
    for i in range(numShots):
        moveDir(f, direction, pitch)
        shoot(f)


"""
Add everything previous to the main body code (movement) to the .vbs file
"""
def addHeader(f):
    f.write("Option Explicit\n\n")
    # First define all variables
    defineVars(f)
            
    # Second enter all used subprocedures and code main body
    with open("body.txt", 'r') as body:	
        for line in body:
            f.write(line)
        

"""
Add everything latter to the main body code (movement) to the .vbs file
"""
def addTrailer(f):
    # Fourth enter what's left to say
    with open("end.txt", 'r') as body:	
        for line in body:
            f.write(line)


"""	
Von Aussen nach Innen. Erste Linie geht nach Rechts.
Bei aussen nach innen muss der Startpunkt immer links oben sein
dir = 0,1,2,3: Up, Right, Down, Left
!!! sizeX und sizeY muessen Vielfaches von pitch sein! Erstellt vollstaendig
ausfuehrbares vbs skript.

"""

def doRasterfahrtIn(initValues, sizeX, sizeY):
    global fileName
    global startX
    global startY
    global pitch
    direction = 1
    lenX = sizeX
    lenY = sizeY
    setParams(initValues)

    if os.path.isfile(fileName+".vbs"):
        print(
        "\nFile already exists. \nPlease delete the existing one, or choose a new \
name.")
        return

    with open(fileName+".vbs", 'a+') as f:
        addHeader(f)

        moveAbs(f, startX, startY)
        shoot(f)     # first shot
        lineRelShoot(f, direction, lenX, pitch)   # first line to the right

        while(lenY >= pitch):
            direction = (direction + 1) % 4
            if (lenY >= pitch):
                    lineRelShoot(f, direction, lenY, pitch)
            direction = (direction + 1) % 4
            if (lenX >= pitch): 
                    lineRelShoot(f, direction, lenX, pitch)
            lenY -= pitch
            lenX -= pitch

        addTrailer(f)


"""
Von Innen nach aussen. Geht nur vom Zentrum aus. Erste Fahrt geht nach Rechts.
Erstellt vollstaendig ausfuehrbares vbs skript.
"""
def doRasterfahrtOut(initValues, sizeX, sizeY):
    global fileName
    global startX
    global startY
    global pitch
    direction = 0
    lenX = 0
    lenY = 0

    setParams(initValues)

    if os.path.isfile(fileName+".vbs"):
        print(
        "\nFile already exists. \nPlease delete the existing one, or choose a new \
name.")
        return

    with open(fileName+".vbs", 'a+') as f:
        addHeader(f)
        moveAbs(f, startX, startY)
        shoot(f)     # first shot

        while (lenX <= sizeX):
            lenX += pitch
            lenY += pitch
            direction = (direction + 1) % 4
            if (lenX <= sizeX):
                lineRelShoot(f, direction, lenX, pitch)
            else:
                lineRelShoot(f, direction, lenX - pitch, pitch)
                break
            direction = (direction + 1) % 4
            if (lenY <= sizeY):
                lineRelShoot(f, direction, lenY, pitch)
            else:
                lineRelShoot(f, direction, lenY - pitch, pitch)
                break

        addTrailer(f)

"""
Get 3 arrays from GUI: Queue, point shot Array and line shot Array.
Turn into vbs script
"""
def readUserPath(f, queue, pArray, lArray):
    lenQ = len(queue)
    i = 0
    while (i < lenQ):
        idx = queue[i][1]  
        if (queue[i][0] == 1):
            # Line
            x0 = lArray[idx][0]
            y0 = lArray[idx][1]
            x1 = lArray[idx][2]
            y1 = lArray[idx][3]
            twoDShoot(f, x0, x1, y0, y1)
        elif (queue[i][0] == 0):
            # Point
            x = pArray[idx][0]
            y = pArray[idx][1]
            moveAndShootAbs(f, x, y)  

        i += 1    


"""
output script made out of basic code blocks
Goal: Only one standard form with different values, but different path

"""
def createUserScript(initValues, queue, points, lines):
    global fileName

    setParams(initValues)

    if os.path.isfile(fileName+".vbs"):
        print(
        "\nFile already exists. \nPlease delete the existing one, or choose a new \
name.")
        return

    with open(fileName+".vbs", 'a+') as f:
        addHeader(f)        

        # enter movement and laser procedure
        readUserPath(f, queue, points, lines)
        
        addTrailer(f)
