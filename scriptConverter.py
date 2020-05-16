#!/usr/bin/env python
"""
20/03/20
Take the path entered into the laser GUI and convert it into a visual basic script (.vbs) script
"""

import os
import math
#import pyximport; pyximport.install()



"""
input: Dictionary with variables params and open file object f.
defines variables in .vbs files
"""
def defineVars(params, f):
    with open("textmodule/header.txt", 'r') as body:
        for line in body:
            f.write(line)

    f.write("startX = %.3f\n" %params['startX'])
    f.write("startY = %.3f\n" %params['startY'])
    f.write("startZ = %.3f\n" %params['startZ'])
    f.write("startLeistung = %.2f\n" %params['startLeistung'])
    f.write("pulse = %d\n" %params['pulse'])
    f.write("pulseEnergyVal = %d\n" %params['pulseEnergy'])
    f.write("energyModeVal = %d\n" %params['energyMode'])
    f.write("triggerModeVal = %d\n" %params['triggerMode'])
    f.write("waitMs = %d\n" %params['waitMs'])


"""
Move relative distance in x or y
"""
def moveRel(f, axis, dist):
    f.write("moveRel %s, %.3f\n" %(axis, dist))
    f.write("waituntilinpos %s\n" %(axis))

"""
Move to absolute location in x and y
"""
def moveAbs(f, xPos, yPos):
    f.write("moveAbs %.3f, %.3f\n" %(xPos, yPos))
    f.write("waituntilinpos x,y\n")

"""
Shoot once.
"""
def shoot(f, repRate):
    f.write("PSOPulse pulse, 1000000/%.3f\n\n" %repRate)

	
"""
Move to absolute location in x and y and shoot once
"""
def moveAndShootAbs(f, repRate, x, y):
    moveAbs(f, x, y)
    shoot(f, repRate)



"""
Appends relative x,y distances to be moved to Array to sum them up in a for loop
move into certain direction relative to original position. 0=up, 1=right, 2=down, 3=left
up and right: +
down and left: -
"""
def moveDir(xDistArray, yDistArray, direction, dist):
    if direction == 0:      # up
        xDistArray.append(0)
        yDistArray.append(dist)
    elif direction == 1:      # right
        xDistArray.append(dist)
        yDistArray.append(0)
    elif direction == 2:      # down
        xDistArray.append(0)
        yDistArray.append(-1*dist)
    elif direction == 3:      # left
        xDistArray.append(-1*dist)
        yDistArray.append(0)


"""
Move along a 2D diagonal line and shoot in a certain pitch
"""
def makeXYArray(f, pitch, x0, y0, x1, y1):
    """ for testing:"""
    xIterations = 0
    yIterations = 0
    # Starting position not shot automatically
    xDistArray = []
    yDistArray = []
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
                xDistArray.append(stepX)
                yDistArray.append(0)
            else:
                break

        # Then: Vertically
        for i in range(timesY):
            if (movedY < deltaY):
                yIterations += 1
                movedY += pitch
                xDistArray.append(0)
                yDistArray.append(stepY)
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
                xDistArray.append(stepX)
                yDistArray.append(0)

            elif (movedY < yIdeal):
                yIterations += 1
                movedY += pitch
                xDistArray.append(0)
                yDistArray.append(stepY)

    return xDistArray, yDistArray	



"""
Move along a horizontal or vertical line and shoot in a certain pitch
"""
def lineRelShoot(f, pitch, direction, dist):
    # Starting position not shot automatically
    text = ""
    step = 0
    num = math.ceil(dist / pitch)

    if direction % 2 == 0:
        if direction == 2:      # down
            step = -1*pitch
        else:                   # up
            step = pitch
        text = "lineRelShootY %d, pulse, %.3f\n" %(num,step)
    else:
        if direction == 3:      # left
            step = -1*pitch
        else:                   # right 
            step = pitch
        text = "lineRelShootX %d, pulse, %.3f\n" %(num,step)

    f.write(text)


"""
Add everything previous to the main body code (movement) to the .vbs file
"""
def xyArrayShoot(f, xDistArray, yDistArray):
    numXY = len(xDistArray)
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

    f.write("xyArrayShoot %d\n" %numXY)
    
"""
Add everything previous to the main body code (movement) to the .vbs file
"""
def addHeader(params, f):
    # First define all variables
    defineVars(params, f)
            
    # Second enter all used subprocedures and code main body
    with open("textmodule/body.txt", 'r') as body:	
        for line in body:
            f.write(line)
        

"""
Add everything latter to the main body code (movement) to the .vbs file
"""
def addTrailer(f):
    # Fourth enter what's left to say
    with open("textmodule/end.txt", 'r') as body:	
        for line in body:
            f.write(line)

"""
easter egg for eric
"""

def addBunny(f):
    with open("textmodule/rabbit.txt", 'r') as body:
        for line in body:
            f.write(line)

def addText(f, fileName):
	with open("textmodule/"+fileName+".txt", 'r') as body:
            for line in body:
                    f.write(line)

"""	
Output is a .vbs script to do a Rasterfahrt (Snail) from
the outside to the inside.
!!! sizeX and sizeY need to be divisible by the pitch.

Starting point:     Upper left corner.
Starting direction: To the right.

dir = 0,1,2,3: Up, Right, Down, Left

NOTE:   - sizeX and sizeY need to be divisible by the pitch.
        - area needs to be quadratic (sizeX = sizeY)
"""

def doRasterfahrtIn(params):
    sizeX = params["sizeX"]
    sizeY = params["sizeY"]
    fileName = params["fileName"]
    startX = params["startX"]
    startY = params["startY"]
    pitch = params["pitch"]
    repRate = params["repRate"]
    origin = params["origin"]
    
    x0 = origin[0]
    y0 = origin[1]

    direction = 1
    lenX = sizeX
    lenY = sizeY


#    if os.path.isfile(fileName+".vbs"):
#        print(
#        "\nFile already exists. \nPlease delete the existing one, or choose a new \
#name.")
#        return
#

    with open(fileName+".vbs", 'w') as f:
        if ("ase" or "unny" or "abbit") in fileName:
            addBunny(f)
        addHeader(params, f)

        # First move to origin (Alignment point). Then move to starting point
        moveAbs(f, startX, startY)
        shoot(f,repRate)     # first shot
        lineRelShoot(f, pitch, direction, lenX)   # first line to the right

        for i in range(math.ceil(sizeX/pitch)):
           direction = (direction + 1) % 4
           lineRelShoot(f, pitch, direction, lenY)
           direction = (direction + 1) % 4
           lineRelShoot(f, pitch, direction, lenX)
           lenY -= pitch
           lenX -= pitch
        
#        while(lenY >= pitch):
#            direction = (direction + 1) % 4
#            if (lenY > 0):
#                lineRelShoot(f, pitch,direction, lenY)
#            direction = (direction + 1) % 4
#            if (lenX > 0): 
#                lineRelShoot(f, pitch, direction, lenX)
#            if (lenY <= 0 or lenX <= 0):
#                break
#
#            lenY -= pitch
#            lenX -= pitch

        addTrailer(f)


"""
Von Innen nach aussen. Geht nur vom Zentrum aus. Erste Fahrt geht nach Rechts.
Erstellt vollstaendig ausfuehrbares vbs skript.
funktioniert nur fuer mehr oder weniger quadratische Formen
"""
def doRasterfahrtOut(params):
    sizeX = params["sizeX"]
    sizeY = params["sizeY"]
    fileName = params["fileName"]
    startX = params["startX"]
    startY = params["startY"]
    pitch = params["pitch"]
    repRate = params["repRate"]
    origin = params["origin"]
    
    x0 = origin[0]
    y0 = origin[1]

    direction = 0
    lenX = 0
    lenY = 0

#    if os.path.isfile(fileName+".vbs"):
#        print(
#        "\nFile already exists. \nPlease delete the existing one, or choose a new \
#name.")
#        return

    with open(fileName+".vbs", 'w') as f:
        print(fileName)
        if ("ase" or "unny" or "abbit") in fileName:
            addBunny(f)
            print("yes")
        addHeader(params, f)
        # moveAbs(f, startX, startY)
        moveRel(f, 'x', startX-x0)
        moveRel(f, 'y', startY-y0)
        shoot(f, repRate)     # first shot


        while (lenX <= sizeX):
            lenX += pitch
            lenY += pitch
            direction = (direction + 1) % 4
            if (lenX <= sizeX):
                lineRelShoot(f, pitch, direction, lenX)
            else:
                lineRelShoot(f, pitch, direction, lenX - pitch)
            direction = (direction + 1) % 4
            if (lenY <= sizeY):
                lineRelShoot(f, pitch, direction, lenY)
            else:
                lineRelShoot(f, pitch, direction, lenY - pitch)
                break

        addTrailer(f)




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
def readUserPath(f, pitch, repRate, queue, pArray, lArray):
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
            # if vertical
            if (x0 == x1):
                yDist = y1 - y0
                if (yDist > 0):
                    direction = 0
                else:
                    direction = 2
                lineRelShoot(f, pitch, direction, abs(yDist))
            # if horizontal    
            elif (y0 == y1):
                xDist = x1 - x0
                if (xDist > 0):
                    direction = 1
                else:
                    direction = 2
                lineRelShoot(f, pitch, direction, abs(xDist))
            # if diagonal
            else:
                xDistArray, yDistArray = makeXYArray(f, pitch, x0, y0, x1, y1)
                xyArrayShoot(f, xDistArray, yDistArray)
        elif (queue[i][0] == 0):
            # Point
            x = pArray[idx][0]
            y = pArray[idx][1]
            moveAndShootAbs(f, repRate, x, y)  

        i += 1    


"""
output script made out of basic code blocks
Goal: Only one standard form with different values, but different path
"""
def createUserScript(params, queue, points, lines):
    fileName = params["fileName"]
    pitch = params["pitch"]

    if os.path.isfile(fileName+".vbs"):
        print(
        "\nFile already exists. \nPlease delete the existing one, or choose a new \
name.")
        return

    with open(fileName+".vbs", 'a+') as f:
        if ("ase" or "unny" or "abbit") in fileName:
            addBunny(f)

        addHeader(params, f)        

        # enter movement and laser procedure
        readUserPath(f, pitch, queue, points, lines)
        
        addTrailer(f)
    return testArray
