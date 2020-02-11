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



	
