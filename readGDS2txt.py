#!/usr/bin/env python
"""
16/01/20
Read file from klayout saved as GDS2-txt files and return list of coordinates for
scriptConverter.py
"""

import os
import math
#import pyximport; pyximport.install()

	
""" 
Read GDS2 txt. file and return UNIT.
"""
def getUnit(path):
    l = 0
    with open(path, 'r') as f:
        for line in f:
            l += 1
            # unit = -1 if unit is smaller than 1 micron.
            if ("UNITS" in line):
                split = line.split(" ")
                unit = float(split[1])*float(split[2])
                print(split[1])
                print(split[2])
                if (unit < 1e-6):
                    return -1   # Error. Unit too small
                else:
                    if (unit == 1e-3):
                        return 1e0
                    else:
                        return unit*1e3
            elif (l == 6):
                return 0  # Error. unit not found


""" 
Read GDS2 txt. file and return path to follow in coordinates
Returns 3 arrays: queue, pArray and lArray.

queue (Nx2): Column 1: Point(0) or line(1), Column 2: Idx of p or l array
(queue basically works as pointer)
pArray (NPx2): C1: x, C2: y
qArray (NQx4): C1,2: x0, y0; C3,4: x1, y1
"""
def getCoordinates(path):
    lineOngoing = 0
    queue = []
    pArray = []
    lArray = []
    pIdx = 0
    lIdx = 0
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0

    with open(path, 'r') as f:
        for line in f:
            if ("ENDEL" in line):
                lineOngoing = 0

            elif (lineOngoing == 1):
                x0 = x1
                y0 = y1
                split = line.split(" ")
                x1 = int(split[0][:-1])
                y1 = int(split[1][:-1])
                queue.append([1, lIdx])
                lArray.append([x0, y0, x1, y1])
                lIdx += 1

            elif ("XY" in line):
                lineOngoing = 1
                split = line.split(" ")
                x0 = int(split[1][:-1])
                y0 = int(split[2][:-1])
                queue.append([0, pIdx])
                pArray.append([x0, y0])
                pIdx += 1
                x1 = x0
                y1 = y0

    return queue, pArray, lArray



	

"""
Move absolute distance in x and y
"""
def moveAbs(f, xPos, yPos):
    f.write("\nmove x, %f\n" %xPos)
    f.write("move y, %f\n" %yPos)
    f.write("waituntilinpos x,y\n")
    f.write("wait waitMs\n")


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
#   V    print(
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
                lineRelShoot(f, direction, lenX)
                # for graphic test
                if (direction == 3):
                    x1 = x0 - lenX
                else:    
                    x1 = x0 + lenX
                testArray.append([x1, y1]) 
                x0 = x1
                y0 = y1
            else:
                lineRelShoot(f, direction, lenX - pitch)
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
                lineRelShoot(f, direction, lenY)
                # for graphic test
                if (direction == 0):
                    y1 = y0 - lenY
                else:    
                    y1 = y0 + lenY
                testArray.append([x1, y1]) 
                x0 = x1
                y0 = y1
            else:
                lineRelShoot(f, direction, lenY - pitch)
                # for graphic test
                if (direction == 0):
                    y1 = y0 - (lenY - pitch)
                else:    
                    y1 = y0 + (lenY - pitch)
                testArray.append([x1, y1]) 
                x0 = x1
                y0 = y1
                break

        addTrailer(f)

    return testArray

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

