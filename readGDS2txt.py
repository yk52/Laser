#!/usr/bin/env python
"""
16/01/20
Read file from klayout saved as GDS2-txt files and return list of coordinates for
scriptConverter.py
Does nothing with the units! 
"""

import os
import math
#import pyximport; pyximport.install()

pathDict = {} 
strucDict = {} 
arrDict = {} 

"""
read whole GDS2 file
"""
def readFile(filePath):
    skipLines = 0
    pathFound = 0
    xy = []
    strname = ""
    x = 0
    y = 0
    with open(filePath, 'r') as f:
        unitFound = 0
        for l, line in enumerate(f): # l = 5 is 6th line
            if (skipLines != 0):
                skipLines -= 1
                continue

            if ("STRNAME" in line):
                split = line.split(" ") 
                strname = split[1]
                continue

            if ("PATH" in line):
                pathFound = 1
                skipLines = 4 # skip right to coordinates
                continue

            if (pathFound == 1):
                split = line.split(" ")
                if ("XY" in line):    
                    x = int(split[1].replace(":",""))
                    y = int(split[2])
                    xy.append((x,y))
                    continue
                if ("ENDEL" in line):
                    path = {strname : tuple(xy)}
                    pathDict.update(path)
                    pathFound = 0
                    strname = ""
                    xy = []
                    continue
                else:
                    x = int(split[0].replace(":",""))
                    y = int(split[1])
                    xy.append((x,y))
                    continue






	

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



	
