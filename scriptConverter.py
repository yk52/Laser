#!/usr/bin/env python
"""
19/11/19
Take the path entered into the laser GUI and convert it into a visual basic script (.vbs) script
"""

import os
import math
#import pyximport; pyximport.install()

# global variables
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
pitchArray = 0

def readGrid(grid):
    # get grid and turn into 2 arrays: start and stop
    return coordinates
	
"""
Sets global parameters for all functions to use.
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
Move a relative distance in x and y and shoot once at that position
"""
def moveRel(f, xDist, yDist):
    f.write("\nmoveRel x, %f\n" %xDist)
    f.write("moveRel y, %f\n" %yDist)
    f.write("waituntilinpos x,y\n")
    f.write("wait waitMs\n")

"""
Move absolute distance in x and y and shoot once at that position
"""
def moveAbs(f, xPos, yPos):
    f.write("\nmove x, %f\n" %xPos)
    f.write("move y, %f\n" %yPos)
    f.write("waituntilinpos x,y\n")
    f.write("wait waitMs\n")
        

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
	

def shoot(f):
    global repRate
    f.write("PSOPulse pulse, 1000000/%f\n" %repRate)

def moveAndShootRel(f, xDist, yDist):
    moveRel(f, xDist, yDist)
    shoot(f)
	
def diagonalShoot(f, x0, x1, y0, y1, pitch):
    # TODO implement diagonal later. continue with for loop
    deltaX = x1 - x0
    deltaY = y1 - y0
    dist = math.sqrt(pow(deltaX,2)+pow(deltaY,2))
    numShots = dist / pitch
	
"""
Move along a horizontal or vertical line and shoot in a certain pitch
"""
def lineRelShoot(f, direction, dist, pitch):
    # Starting position not shot automatically
    # 0 = start, 1 = stop
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

def doRasterfahrtIn(initValues, sizeX, sizeY, pitch):
    global fileName
    global startX
    global startY
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
def doRasterfahrtOut(initValues, sizeX, sizeY, pitch):
    global fileName
    global startX
    global startY
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
output script made out of basic code blocks
Goal: Only one standard form with different values, but different path

"""
def createUserScript(initValues, coordinates):
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
        arrayLen = len(coordinates)-1
        for i in range(0, arrayLen+1):
            moveAndShootRel(f, coordinates[i][0], coordinates[i][1])
        
        addTrailer(f)
