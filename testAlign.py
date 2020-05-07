#!/usr/bin/env python
"""
test script for scriptConverter
precision: 1 micron. Base unit is 1 mm. E.g. enter number in microns and add E-3?
"""
import alignment

x1 = 39.29
y1 = -61.143

x2 = 112.8
y2 = -64.82

p1 = (x1,y1)
p2 = (x2,y2)

alignment.removeTilt(p2, p1)
