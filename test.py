#!/usr/bin/env python
"""
test script for scriptConverter
enter mm! i.e. Microns and add E-3 
"""
import readGDS2txt
import scriptConverter

fileName = "letsShoot"
""" alignment point in erics design
x0 = -36800E-3
y0 = -2800E-3
"""
# origin on wafer (seen trough laser)
x0 = 41.447 + 1.971 + 0.226
y0 = -57.055 - 114.746 - 1.066

# start point. Don't forget to add offset to site!
x = 100.291 + 0.226
y = -162.814 - 1.066

z = 3.0
startLeistung = -26
pulse = 1
repRate = 20 
pulseEnergy = 220
energyMode = 0
triggerMode = 0
waitMs = 100
pitch = 1
overlap = 0

sizeX = 10
sizeY = 10

origin = (x0, y0)

# newPitch = pitch - overlap
pitch -= overlap

params = {"origin":origin, "overlap":overlap, "fileName":fileName, "startX":x, "startY":y, "startZ":z,\
        "startLeistung":startLeistung, "pulse":pulse, "repRate":repRate,\
        "pulseEnergy":pulseEnergy, \
        "energyMode":energyMode, "triggerMode":triggerMode,\
        "waitMs":waitMs, "pitch":pitch, "sizeX":sizeX, "sizeY":sizeY}

scriptConverter.doRasterfahrtIn(params)
