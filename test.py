#!/usr/bin/env python
"""
test script for scriptConverter
"""
import readGDS2txt
import scriptConverter

x = 0
y = 0
z = 0
startLeistung = -26
pulse = 1
repRate = 20 
pulseEnergy = 220
hv = 26
energyMode = 0
triggerMode = 0
waitMs = 100
pitch = 10

sizeX = 40
sizeY = 60

params = {"fileName":"unny", "startX":x, "startY":y, "startZ":z,\
        "startLeistung":startLeistung, "pulse":pulse, "repRate":repRate,\
        "pulseEnergy":pulseEnergy, "hv":hv,\
        "energyMode":energyMode, "triggerMode":triggerMode,\
        "waitMs":waitMs, "pitch":pitch, "sizeX":sizeX, "sizeY":sizeY}
#queue = [[0,0],[1,0],[1,1],[1,2],[1,3],[0,1]]
#p = [[0,0],[4,2]]
#l = [[0,0,2,0],[2,0,2,3],[2,3,1,3],[1,3,1,2]]
scriptConverter.doRasterfahrtOut(params)

#queue, p, l = readGDS2txt.getCoordinates("test2.txt")
#print(queue)
#print(p)
#print(l)
#scriptConverter.createUserScript(params, queue, p, l)

#with open("twoDTest.txt", 'w') as f:
#    scriptConverter.twoDShoot(f, 0, 5, 0, 5)
