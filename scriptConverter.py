#!/usr/bin/env python
"""
09/01/20
Take the path entered into the laser GUI and convert it into a visual basic script (.vbs) script
"""

import os
import math
#import pyximport; pyximport.install()

unit = 1.0    # standard unit = 1 mm. Smalles precision: 1 micron

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
pitch = 20   

# Arrays of single line with relative distances to be moved
xDistArray = []
yDistArray = []

# delete later
testArray = []
testX = 0
testY = 0

	
"""
Sets global parameters from GUI input for all functions to use
"""
def setParams(array):
    # Maybe it was a mistake to use global variables.........
    global fileName
    global unit
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
    unit = array[i]   # unit size relative to mm
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
    global unit
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
    f.write("dim unit, startX, startY, startZ, startLeistung\n")
    f.write("dim xArray, yArray, lenArray\n")
    f.write("dim pulse\n")
    f.write("dim i,j\n")
    f.write("dim pulseEnergyDist, HVVal, energyModeVal, triggerModeVal\n")
    f.write("dim waitMs\n\n")
    f.write("unit = %.3E\n" %unit)
    f.write("startX = %.3f\n" %startX)
    f.write("startY = %.3f\n" %startY)
    f.write("startZ = %.3f\n" %startZ)
    f.write("startLeistung = %.2f\n" %startLeistung)
    f.write("pulse = %d\n" %pulse)
    f.write("pulseEnergyDist = %d\n" %pulseEnergy)
    f.write("HVVal = %d\n" %hv)
    f.write("energyModeVal = %d\n" %energyMode)
    f.write("triggerModeVal = %d\n" %triggerMode)
    f.write("waitMs = %d\n\n" %waitMs)
	
def shoot(f):
    global repRate
    f.write("PSOPulse pulse, 1000000/%.3f\n" %repRate)
    

"""
Move a relative distance in x and y
"""
def moveRel(f, xDist, yDist):
    f.write("\nmoveRel x, %.3f*unit\n" %xDist)
    f.write("moveRel y, %.3f*unit\n" %yDist)
    f.write("waituntilinpos x,y\n")
    f.write("wait waitMs\n")

"""
Move absolute distance in x and y
"""
def moveAbs(f, xPos, yPos):
    f.write("\nmove x, %.3f*unit\n" %xPos)
    f.write("move y, %.3f*unit\n" %yPos)
    f.write("waituntilinpos x,y\n")
    f.write("wait waitMs\n")

"""
Shoot once.
"""
def shoot(f):
    global repRate
    f.write("PSOPulse pulse, 1000000/%.3f\n" %repRate)


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
    global testX, testY, testArray #delete later
    moveAbs(f, x, y)
    shoot(f)

    #delete later
    testX = x
    testY = y
    testArray.append([testX, testY])
        

"""
move into certain direction. 0=up, 1=right, 2=down, 3=left
up and right: +
down and left: -
"""
def moveDir(f, direction, dist):
    if direction == 0:      # up
        moveRel(f, 0, dist)
    elif direction == 1:      # right
        moveRel(f, dist, 0)
    elif direction == 2:      # down
        moveRel(f, 0, -1*dist)
    elif direction == 3:      # left
        moveRel(f, -1*dist, 0)
	

def moveRelArray(xDist, yDist):        
    xDistArray.append(xDist)
    yDistArray.append(yDist)

    # delete later
    global testX, testY, testArray
    testX += xDist
    testY += yDist
    testArray.append([testX, testY])

"""
Appends relative x,y distances to be moved to Array to sum them up in a for loop
move into certain direction relative to original position. 0=up, 1=right, 2=down, 3=left
up and right: +
down and left: -
"""
def moveDirArray(direction, dist):
    if direction == 0:      # up
        moveRelArray(0, dist)
    elif direction == 1:      # right
        moveRelArray(dist, 0)
    elif direction == 2:      # down
        moveRelArray(0, -1*dist)
    elif direction == 3:      # left
        moveRelArray(-1*dist, 0)

"""
Move along a 2D (possibly diagonal) line and shoot in a certain pitch
"""
def lineShootArray(f, x0, y0, x1, y1):
    """ for testing:"""
    global pitch
    xIterations = 0
    yIterations = 0
    # Starting position not shot automatically
    deltaX = float(x1 - x0)
    deltaY = float(y1 - y0)

    x = x0
    y = y0
    
    if (deltaY < 0):
        stepY = -1 * pitch 
        deltaY = -1 * deltaY
    else:
        stepY = pitch


    if (deltaX < 0):
        stepX = -1 * pitch
        deltaX = -1 * deltaX
    else:
        stepX = pitch

    slope = deltaY / deltaX
    idealStepY = pitch * slope # absolute value

    if (idealStepY >= pitch):
        timesX = 1
        timesY = math.ceil(idealStepY / pitch)
        correctX = 1
        diff = abs(idealStepY - pitch*timesY)
        if (diff == 0):
            checkTimes = 0
        else:
            checkTimes = math.ceil(idealStepY/diff)
    elif (idealStepY < pitch):
        timesY = 1
        timesX = math.ceil(pitch / idealStepY)
        correctY = 1
        diff = abs(idealStepY - pitch*timesX)
        checkTimes = math.ceil(diff/idealStepY)

    movedX = 0
    movedY = 0

    # deltaX and Y are absolutes now
    while ((movedX < deltaX) or (movedY < deltaY)):
        # First: Do step sideways
        for i in range(timesX):
            if (movedX < deltaX):
                xIterations += 1
                movedX += pitch
                moveRelArray(stepX, 0)
            else:
                break

        # Then: Vertically
        for i in range(timesY):
            if (movedY < deltaY):
                yIterations += 1
                movedY += pitch
                moveRelArray(0, stepY)
            else:
                break

        # Add correction steps if needed
        if (checkTimes != 0 and (min(xIterations, yIterations) % checkTimes ==
            0)):
            xIdeal = (yIterations * pitch) / slope
            yIdeal = slope * (xIterations * pitch)

            if (movedX < xIdeal):
                xIterations += 1
                movedX += pitch
                moveRelArray(stepX, 0)

            elif (movedY < yIdeal):
                yIterations += 1
                movedY += pitch
                moveRelArray(0, stepY)

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
Move along a horizontal or vertical line and shoot in a certain pitch
"""
def lineRelShootArray(direction, dist):
    # Starting position not shot automatically
    # 0 = start, 1 = stop
    global pitch
    numShots = int(dist / pitch)
    for i in range(numShots):
        moveDirArray(direction, pitch)

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
Add everything previous to the main body code (movement) to the .vbs file
"""
def addForLoop(f):
    numXY = len(xDistArray)
    f.write("lenArray = %d\n" %numXY)
    f.write("xDistArray = Array(")
    i = 0
    for x in xDistArray:
        f.write(str(x))
        i += 1
        if (i != numXY):
            f.write(", ")
        else:
            f.write(")\n")

    f.write("yDistArray = Array(")
    i = 0
    for y in yDistArray:
        f.write(str(y))
        i += 1
        if (i != numXY):
            f.write(", ")
        else:
            f.write(")\n")

    with open("singleLine.txt", 'r') as body:	
        for line in body:
            f.write(line)
        f.write("\n")    

"""
Add everything latter to the main body code (movement) to the .vbs file
"""
def addTrailer(f):
    # Fourth enter what's left to say
    with open("end.txt", 'r') as body:	
        for line in body:
            f.write(line)

def addBunny(f):
    with open("rabbit.txt", 'r') as body:
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
        if ("ase" or "unny" or "abbit") in fileName:
            addBunny(f)
        addHeader(f)

        moveAbs(f, startX, startY)
        shoot(f)     # first shot
        lineRelShootArray(direction, lenX)   # first line to the right

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
                lineRelShootArray(direction, lenY)
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
                lineRelShootArray(direction, lenX)
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

    
        addForLoop(f)
        addTrailer(f)

        return testArray


"""
Von Innen nach aussen. Geht nur vom Zentrum aus. Erste Fahrt geht nach Rechts.
Erstellt vollstaendig ausfuehrbares vbs skript.
funktioniert nur fuer mehr oder weniger quadratische Formen
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
    testArray = []
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
        if ("ase" or "unny" or "abbit") in fileName:
            addBunny(f)
            print("yes")
        addHeader(f)
        moveAbs(f, startX, startY)
        shoot(f)     # first shot

        #for graphic test
        testArray.append([startX, startY])
        x0 = startX
        y0 = startY

        while (lenX <= sizeX):
            lenX += pitch
            lenY += pitch
            direction = (direction + 1) % 4
            if (lenX <= sizeX):
                lineRelShootArray(direction, lenX)
                # for graphic test
                if (direction == 3):
                    x1 = x0 - lenX
                else:    
                    x1 = x0 + lenX
                testArray.append([x1, y1]) 
                x0 = x1
                y0 = y1
            else:
                lineRelShootArray(direction, lenX - pitch)
                # for graphic test
                if (direction == 3):
                    x1 = x0 - (lenX - pitch)
                else:    
                    x1 = x0 + (lenX - pitch)
                testArray.append([x1, y1]) 
                x0 = x1
                y0 = y1
                break
            direction = (direction + 1) % 4
            if (lenY <= sizeY):
                lineRelShootArray(direction, lenY)
                # for graphic test
                if (direction == 0):
                    y1 = y0 - lenY
                else:    
                    y1 = y0 + lenY
                testArray.append([x1, y1]) 
                x0 = x1
                y0 = y1
            else:
                lineRelShootArray(direction, lenY - pitch)
                # for graphic test
                if (direction == 0):
                    y1 = y0 - (lenY - pitch)
                else:    
                    y1 = y0 + (lenY - pitch)
                testArray.append([x1, y1]) 
                x0 = x1
                y0 = y1
                break

        addForLoop(f)
        addTrailer(f)

    return testArray


def clearRelArrays():
    global xDistArray, yDistArray
    xDistArray = []
    yDistArray = []

"""
Get 3 arrays from GUI: Queue, point shot Array and line shot Array.
Turn into vbs script
unit must be already converted such that the coordinates*unit == [mm]

Array contents:
    Queue ->    Required actions in chronological order. 
                Column1: Point(0) or line(1), Column2: index of position in p or
                lArray where coordinates are saved
    pArray ->   [xCoordinate, yCoordinate]
    lArray ->   [x0, y0, x1, y1] 0=start, 1=goal
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
            if (x0 == x1):
                yDist = y1 - y0
                if (yDist > 0):
                    direction = 0
                else:
                    direction = 2
                lineRelShootArray(direction, abs(yDist))
            elif (y0 == y1):
                xDist = x1 - x0
                if (xDist > 0):
                    direction = 1
                else:
                    direction = 2
                lineRelShootArray(direction, abs(xDist))
            else:
                lineShootArray(f, x0, y0, x1, y1)
            if (i == lenQ - 1):    
                addForLoop(f)
        elif (queue[i][0] == 0):
            # Point
            if (i != 0):
                addForLoop(f)
            clearRelArrays()
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
    global testArray #delete later

    setParams(initValues)

    if os.path.isfile(fileName+".vbs"):
        print(
        "\nFile already exists. \nPlease delete the existing one, or choose a new \
name.")
        return

    with open(fileName+".vbs", 'a+') as f:
        if ("ase" or "unny" or "abbit") in fileName:
            addBunny(f)

        addHeader(f)        

        # enter movement and laser procedure
        readUserPath(f, queue, points, lines)
        
        addTrailer(f)
    return testArray
