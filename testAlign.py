#!/usr/bin/env python
"""
test script for scriptConverter
precision: 1 micron. Base unit is 1 mm.
"""
import alignment

p1 = (4,-1)
p2 = (0,-1)

alignment.removeTilt(p2, p1)
