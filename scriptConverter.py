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
pitch = 1   

	
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
def diagonalShoot(f, x0, y0, x1, y1):
    """ for testing:"""
    testArray = []

    global pitch
    # Starting position not shot automatically
    deltaX = float(x1 - x0)
    deltaY = float(y1 - y0)
    slope = deltaY / deltaX

    if (deltaX < 0):
        stepX = -1 * pitch
        deltaX *= -1
    else:
        stepX = pitch

    if (deltaY < 0):
        stepY = -1 * pitch
        deltaY *= -1
        fac = -1
    else:
        stepY = pitch

    idealStepY = stepX * slope
    x = x0
    y = y0
    yIdeal = y0


    while (deltaY > 0 or deltaX > 0):
        diffIdeal = abs(yIdeal - y)

        if (deltaX > 0 and diffIdeal < 0):
            deltaX -= abs(stepX)
            x += stepX
            moveAndShootAbs(f, x, y)
            testArray.append([x,y]) # delete later
            print(x,y)

            if (deltaY > 0):
                yIdeal = yIdeal + idealStepY
                print(yIdeal)

        
        diffIdeal = abs(yIdeal - y)
        if (deltaY > 0 and diffIdeal > 0):
            deltaY -= abs(stepY)
            y += stepY
            moveAndShootAbs(f, x, y)
            testArray.append([x,y]) # delete later
            print("y")
            print(x,y)


    return testArray        
                
	

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


#    if os.path.isfile(fileName+".vbs"):
#        print(
#        "\nFile already exists. \nPlease delete the existing one, or choose a new \
#name.")
#        return
#
    #TODO for graphic Test
    testArray = []

    with open(fileName+".vbs", 'a+') as f:
        addHeader(f)

        moveAbs(f, startX, startY)
        shoot(f)     # first shot
        lineRelShoot(f, direction, lenX)   # first line to the right

        # for graphic Test:
        x0 = startX
        y0 = startY
        x1 = x0 + lenX
        y1 = startY
        testArray.append([x0, y0])
        testArray.append([x1, y1])
        x0 = x1
        y0 = y1

        while(lenY >= pitch):
            direction = (direction + 1) % 4
            if (lenY >= pitch):
                lineRelShoot(f, direction, lenY)
                # for graphic test
                x1 = x0
                if (direction == 0):
                    y1 = y0 - lenY
                else:    
                    y1 = y0 + lenY
                testArray.append([x1, y1]) 
                x0 = x1
                y0 = y1
            direction = (direction + 1) % 4
            if (lenX >= pitch): 
                lineRelShoot(f, direction, lenX)
                # for graphic test
                y1 = y0
                if (direction == 3):
                    x1 = x0 - lenX
                else:    
                    x1 = x0 + lenX
                testArray.append([x1, y1]) 
                x0 = x1
                y0 = y1
            lenY -= pitch
            lenX -= pitch

        addTrailer(f)

        return testArray


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

    # for graphic Test:
    x0 = startX
    y0 = startY
    x1 = x0 + lenX
    y1 = startY
    testArray.append([x0, y0])
    testArray.append([x1, y1])
    x0 = x1
    y0 = y1

#    if os.path.isfile(fileName+".vbs"):
#        print(
#        "\nFile already exists. \nPlease delete the existing one, or choose a new \
#name.")
#        return

    with open(fileName+".vbs", 'a+') as f:
        addHeader(f)
        moveAbs(f, startX, startY)
        shoot(f)     # first shot

        while (lenX <= sizeX):
            lenX += pitch
            lenY += pitch
            direction = (direction + 1) % 4
            if (lenX <= sizeX):
                lineRelShoot(f, direction, lenX)
            else:
                lineRelShoot(f, direction, lenX - pitch)
                break
            direction = (direction + 1) % 4
            if (lenY <= sizeY):
                lineRelShoot(f, direction, lenY)
            else:
                lineRelShoot(f, direction, lenY - pitch)
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
            diagonalShoot(f, x0, x1, y0, y1)
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
