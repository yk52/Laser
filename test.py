#!/usr/bin/env python
"""
test script for scriptConverter
enter mm! i.e. Microns and add E-3 
"""
import readGDS2txt
import scriptConverter

fileName = "liftOff"

# alignment point/origin in erics design
x0D = -36800E-3
y0D = -2800E-3

# start point in erics design
xD = 46.639
yD = -167.073

# alignment point/origin on wafer (seen trough laser)
x0 = 46.595
y0 = -152.341


# Calculate relative distance from origin to starting point
moveXRel = xD - x0D
moveYRel = yD - y0D

xStart = x0 + moveXRel
yStart = y0 + moveYRel

z = 3.05
startLeistung = -26
pulse = 1
repRate = 20 
pulseEnergy = 220
energyMode = 0
triggerMode = 0
waitMs = 100
pitch = 0.200
overlap = 0

sizeX = 5
sizeY = 5

origin = (x0, y0)

# newPitch = pitch - overlap
pitch -= overlap

params = {"origin":origin, "overlap":overlap, "fileName":fileName, "startX":startX, "startY":startY, "startZ":z,\
        "startLeistung":startLeistung, "pulse":pulse, "repRate":repRate,\
        "pulseEnergy":pulseEnergy, \
        "energyMode":energyMode, "triggerMode":triggerMode,\
        "waitMs":waitMs, "pitch":pitch, "sizeX":sizeX, "sizeY":sizeY}

scriptConverter.doRasterfahrtIn(params)
