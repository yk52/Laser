#!/usr/bin/env python
"""
16/05/20
Take the path entered into the laser GUI and convert it into a visual basic script (.vbs) script
"""

import os
import math
#import pyximport; pyximport.install()



"""
input:  params: Dictionary with variables
        f:      Open file object

effect: defines variables in f
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
input:  axis:   x or y (char)
        f:      Open file object
        dist:   Distance to be moved in mm (float)

effect: Writes move function for relative distance in x or y
        into f
"""
def moveRel(f, axis, dist):
    f.write("moveRel %s, %.3f\n" %(axis, dist))
    f.write("waituntilinpos %s\n" %(axis))



"""
input:  xPos:   Absolute xPosition in laser coordinates in mm (float)
        yPos:   Absolute yPosition in laser coordinates in mm (float)
        f:      Open file object

effect: Writes move function to absolute x and y position
        into f
"""
def moveAbs(f, xPos, yPos):
    f.write("moveAbs %.3f, %.3f\n" %(xPos, yPos))
    f.write("waituntilinpos x,y\n")




"""
input:  repRate: Laser frequency (Hz)
        f:       Open file object

effect: Writes shoot function into f
"""
def shoot(f, repRate):
    f.write("PSOPulse pulse, 1000000/%.3f\n\n" %repRate)




"""
input:  repRate: Laser frequency (Hz)
        f:       Open file object
        x:       Absolute xPosition in laser coordinates in mm (float)
        y:       Absolute yPosition in laser coordinates in mm (float)

effect: Writes shoot and move function into f
"""
def moveAndShootAbs(f, repRate, x, y):
    moveAbs(f, x, y)
    shoot(f, repRate)



"""
input:  xDistArray: Array with relative distances along the x axis
                    ordered chronologically
        yDistArray: Array with relative distances along the y axis
                    ordered chronologically
        direction:  Either 0,1,2 or 3 (= Up, Right, Down or Left)
        dist:       Distance to be moved in mm (float)

effect: Appends relative x,y distances to be moved to an Array to 
        gather them up for a for loop, in order to move into certain
        direction relative to original position. 
"""
def moveDir(xDistArray, yDistArray, direction, dist):
    if direction == 0:      # up: positive
        xDistArray.append(0)
        yDistArray.append(dist)
    elif direction == 1:      # right: positve
        xDistArray.append(dist)
        yDistArray.append(0)
    elif direction == 2:      # down: negative
        xDistArray.append(0)
        yDistArray.append(-1*dist)
    elif direction == 3:      # left: negative
        xDistArray.append(-1*dist)
        yDistArray.append(0)


"""
input:  f:      open file object
        pitch:  Pitch between shots in mm (float)
        x0, y0: Starting postion (first shot) in mm (float)    
        x1, y1: Goal postion (last shot) in mm (float)    

output: xDistArray and yDistArray with relative distances to
        move along a 2D diagonal line and shoot in a certain pitch
"""
def moveDiagonal(f, pitch, x0, y0, x1, y1):
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
input:  f:          open file object
        pitch:      Pitch between shots in mm (float)
        direction:  Either 0,1,2 or 3 (= Up, Right, Down or Left)
        num:        Number of times to be shot at pitch in direction

effect: write move-function to move along a horizontal or vertical line 
        and shoot in a certain pitch into f
"""
def lineRelShoot(f, pitch, direction, num):
    # Starting position not shot automatically
    text = ""
    step = 0

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
input:  f:          open file object
        xDistArray: Array with relative distances along the x axis
                    ordered chronologically
        yDistArray: Array with relative distances along the y axis
                    ordered chronologically

effect: write move-function according to yDistArray and xDistArray
        into f
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
input:  params: Variables as dictionary
        f:      Open file object

effect: Write variable and function definitions into f
"""
def addHeader(params, f):
    # First define all variables
    defineVars(params, f)
            
    # Second enter all used subprocedures and code main body
    with open("textmodule/body.txt", 'r') as body:	
        for line in body:
            f.write(line)
        

"""
input:  f: open file object 

effect: Add text to f
"""
def addImportantStuff(f):
    # Enter what is left to say. 
    with open("textmodule/rabbit.txt", 'r') as body:	
        f.write("\n")
        for line in body:
            f.write(line)
        f.write("\n")


"""
input:  fileName:   filename of textfile you want to copy
        f:          Open file object

effect: copy text of [fileName].txt to f (Generic version of the functions above)
"""
def addText(f, fileName):
	with open("textmodule/"+fileName+".txt", 'r') as body:
            for line in body:
                    f.write(line)

"""	
input:  params: Variables as directory
Output: .vbs script to do a Rasterfahrt (Snail) from
        the outside to the inside.

NOTES_________
!!! sizeX and sizeY need to be divisible by the pitch.
!!! Starting point has to be in upper left corner
!!! Area has to be quadratic (sizeX = sizeY)

Starting direction: To the right.

dir = 0,1,2,3: Up, Right, Down, Left

"""

def doRasterfahrtIn(params):
    size = params["size"]
    fileName = params["fileName"]
    startX = params["startX"]
    startY = params["startY"]
    pitch = params["pitch"]
    repRate = params["repRate"]
    origin = params["origin"]
    
    x0 = origin[0]
    y0 = origin[1]

    direction = 1
    num = int(size/pitch)


#    if os.path.isfile(fileName+".vbs"):
#        print(
#        "\nFile already exists. \nPlease delete the existing one, or choose a new \
#name.")
#        return
#

    with open("Skripte/"+fileName+".vbs", 'w') as f:
        if ("ase" or "uck" or "abbit") in fileName:
            addImportantStuff(f)
        addHeader(params, f)

        # First move to origin (Alignment point). Then move to starting point
        moveAbs(f, startX, startY)
        shoot(f,repRate)     # first shot
        lineRelShoot(f, pitch, direction, num)   # first line to the right

        for i in range(num):
            direction = (direction + 1) % 4
            lineRelShoot(f, pitch, direction, num-i)
            direction = (direction + 1) % 4
            lineRelShoot(f, pitch, direction, num-i)
        



"""
input:  params: Variables as directory
Output: .vbs script to do a Rasterfahrt (Snail) from
        the inside to the outside.

NOTES_________
!!! size needs to be divisible by the pitch.
!!! Starting point has to be in the center.
!!! Area needs to be quadratic (sizeX = sizeY)


Starting direction: To the right.

dir = 0,1,2,3: Up, Right, Down, Left
"""
def doRasterfahrtOut(params):
    size = params["size"]
    fileName = params["fileName"]
    startX = params["startX"]
    startY = params["startY"]
    pitch = params["pitch"]
    repRate = params["repRate"]
    origin = params["origin"]
    
    x0 = origin[0]
    y0 = origin[1]

    direction = 0
    num = int(size/pitch)

#    if os.path.isfile(fileName+".vbs"):
#        print(
#        "\nFile already exists. \nPlease delete the existing one, or choose a new \
#name.")
#        return

    with open("Skripte/"+fileName+".vbs", 'w') as f:
        if ("ase" or "unny" or "abbit") in fileName:
            addImportantStuff(f)
        addHeader(params, f)
        moveAbs(f, startX, startY)
        shoot(f, repRate)     # first shot

        
        for i in range(num):
            direction = (direction + 1) % 4
            lineRelShoot(f, pitch, direction, i+1)
            direction = (direction + 1) % 4
            lineRelShoot(f, pitch, direction, i+1)

        # Last line to fill the square
        direction = (direction + 1) % 4
        lineRelShoot(f, pitch, direction, num)




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
                xDistArray, yDistArray = moveDiagonal(f, pitch, x0, y0, x1, y1)
                xyArrayShoot(f, xDistArray, yDistArray)
        elif (queue[i][0] == 0):
            # Point
            x = pArray[idx][0]
            y = pArray[idx][1]
            moveAndShootAbs(f, repRate, x, y)  

        i += 1    


"""
TODO: In the working. Take gds file (e.g. klayout file) and transform into vbs file.
output script made out of basic code blocks
"""
def createUserScript(params, queue, points, lines):
    fileName = params["fileName"]
    pitch = params["pitch"]

    if os.path.isfile(fileName+".vbs"):
        print("\nFile already exists.\nPlease choose another name.")
        return

    with open("Skripte/"+fileName+".vbs", 'a+') as f:
        if ("ase" or "unny" or "abbit") in fileName:
            addImportantStuff(f)

        addHeader(params, f)        

        # enter movement and laser procedure
        readUserPath(f, pitch, queue, points, lines)
        
    return testArray
