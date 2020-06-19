#!/usr/bin/env python
"""
Create .vbs script for Rasterfahrt (Outside to inside)

Precision:  1 micron. Base unit is 1 mm. E.g. enter number in microns
            and add E-3 or directly as mm.
"""
import scriptConverter




"""
USER INPUTS:
"""
# name for vbs script
fileName = "testSchuss"

# Alignment point/origin in design
x0D = -37
y0D = -2.608

# First intended shooting point in design
xD = -38.439
yD = -2.031

# Alignment point/origin in laser coordinates
x0 = 34.460
y0 = -177.619

# Size of the quadratic to-be-lasered area, pitch and overlap
size = 0.3
pitch = 0.3
overlap = 0

# Other laser parameters
z = 3.1
startLeistung = -26
pulse = 1
repRate = 20 
pulseEnergy = 220
energyMode = 0
triggerMode = 0
waitMs = 100



"""
DO NOT CHANGE THE CODE BELOW
"""
# Calculate relative distance from origin to starting point
moveXRel = xD - x0D
moveYRel = yD - y0D

startX = x0 + moveXRel
startY = y0 + moveYRel


origin = (x0, y0)

pitch -= overlap

params = {"origin":origin, "overlap":overlap, "fileName":fileName, "startX":startX, "startY":startY, "startZ":z,\
        "startLeistung":startLeistung, "pulse":pulse, "repRate":repRate,\
        "pulseEnergy":pulseEnergy, \
        "energyMode":energyMode, "triggerMode":triggerMode,\
        "waitMs":waitMs, "pitch":pitch, "size":size}

#scriptConverter.doRasterfahrtOut(params)
scriptConverter.doRasterfahrtIn(params)
