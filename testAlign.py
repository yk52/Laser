#!/usr/bin/env python
"""
test script for scriptConverter
precision: 1 micron. Base unit is 1 mm. E.g. enter number in microns and add E-3?
"""
import alignment

x1 = 39.101
y1 = -60.939

x2 = 113.007
y2 = -64.627

p1 = (x1,y1)
p2 = (x2,y2)

alignment.removeTilt(p2, p1)
