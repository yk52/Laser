#!/usr/bin/env python
"""
test script for scriptConverter
precision: 1 micron. Base unit is 1 mm. E.g. enter number in microns and add E-3?
"""
import alignment

x1 = 40000E-3
y1 = -10000E-3

x2 = -20000E-3
y2 = 2500E-3

p1 = (x1,y1)
p2 = (x2,y2)

alignment.removeTilt(p2, p1)
