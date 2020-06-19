#!/usr/bin/env python
"""
Create .vbs script for Rasterfahrt (Outside to inside)

Precision:  1 micron. Base unit is 1 mm. E.g. enter number in microns
            and add E-3 or directly as mm.
"""
import readGDS2txt
import scriptConverter




"""
USER INPUTS:
"""
# name for vbs script
fileName = "schnecke5x5"

# Alignment point/origin in design
x0D = -36800E-3
y0D = -2800E-3

# First intended shooting point in design
xD = 46.639
yD = -167.073

# Alignment point/origin in laser coordinates
x0 = 46.595
y0 = -152.341

# Size of the quadratic to-be-lasered area, pitch and overlap
size = 5
pitch = 0.2
overlap = 0

# Other laser parameters
z = 3.05
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
