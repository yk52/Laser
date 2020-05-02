#!/usr/bin/env python
"""
test script for scriptConverter
enter mm! i.e. Microns and add E-3 
"""
import readGDS2txt
import scriptConverter

fileName = "ENDLICH"
# origin
x0 = -36810E-3
y0 = 302E-3
# start point
x = -37400E-3
y = 9990E-3
z = 0E-3
startLeistung = -26
pulse = 1
repRate = 20 
pulseEnergy = 220
hv = 26
energyMode = 0
triggerMode = 0
waitMs = 100
pitch = 100E-3
overlap = 0E-3

sizeX = 1800E-3
sizeY = 1800E-3

origin = (x0, y0)

# newPitch = pitch - overlap
pitch -= overlap

params = {"origin":origin, "overlap":overlap, "fileName":fileName, "startX":x, "startY":y, "startZ":z,\
        "startLeistung":startLeistung, "pulse":pulse, "repRate":repRate,\
        "pulseEnergy":pulseEnergy, "hv":hv,\
        "energyMode":energyMode, "triggerMode":triggerMode,\
        "waitMs":waitMs, "pitch":pitch, "sizeX":sizeX, "sizeY":sizeY}

scriptConverter.doRasterfahrtIn(params)
