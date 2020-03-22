#!/usr/bin/env python
"""
20/03/20
Input: Position of alignment field left and right. XY1, XY2 (The ones furthest outside.)
Output: VBS script for alignment to get global coordinate system without tilt.
"""

import os
import numpy as np

"""
Input:  point 1 and 2 (p1, p2 in (x,y) as tuple). 
Output: Correction Angle in degrees so that both points are at the same y value.
        Correction Angle is already into correct direction (CCW is positive)
"""
def calcCorrAngle(p1,p2):
    dX = p1[0] - p2[0]
    dY = p1[1] - p2[1]
    rad = -1*np.arctan(dY/dX)
    return np.degrees(rad)


"""
Input:  p1, p2
Output: euclidean distance between p1, p2
"""
def calcDist(p1, p2):
    a = np.array(p1)
    b = np.array(p2)
    return np.linalg.norm(a-b)


"""
Input:  open file to write to
Output: Writes header into file
"""
def addText(f, fileName):
    with open("textmodule/"+fileName+".txt", 'r') as body:
        for line in body:
            f.write(line)

"""
Input:  f: open file object
        p: point tuple
        corrAngle: correction Angle in degrees
        dist: euclidean distance between alignment points p1 and p2
"""
def defineVars(f, p, corrAngle, dist):
    f.write("\nx1 = %.3f\ny1 = %.3f" %(p[0], p[1]))
    f.write("\ncorrAngle = %.3f\ndist = %.3f\n" %(corrAngle, dist))


"""
Input:  Correction angle, p1, p2 = (x,y)
Output: Script which removes the tilt from coordinate system
        Execute script and check if it aligned. If not: repeat?
"""
def removeTilt(p1, p2):
    dist = calcDist(p1, p2)
    corrAngle = calcCorrAngle(p1, p2)
    # choose leftmost point
    if (p1[0] < p2[0]):
        p = p1
    else:
        p = p2

    with open("alignment.vbs", 'w') as f:
        addText(f, "alignmentHeader")
        defineVars(f, p, corrAngle, dist)
        addText(f, "alignmentBody")


