#!/usr/bin/env python
"""
16/05/20
Create .vbs script for alignment. Removes the tilt.

Precision:  1 micron. Base unit is 1 mm. E.g. enter number in microns and add E-3
            or directly as mm.
"""
import alignment

# USER INPUT: Left alignment point (mm)
x1 = 39.101
y1 = -60.939

# USER INPUT: Right alignment point (mm)
x2 = 113.007
y2 = -64.627




#### DO NOT CHANGE THE CODE BELOW
p1 = (x1,y1)
p2 = (x2,y2)

alignment.removeTilt(p2, p1)
####
