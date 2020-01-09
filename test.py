#!/usr/bin/env python
"""
test script for scriptConverter
"""
import readGDS2txt
import scriptConverter

x = 10
y = 10
z = 10
startLeistung = -26
pulse = 1
repRate = 20 
PulseEnergy = 220
hv = 26
EnergyMode = 0
TriggerMode = 0
waitMs = 100
pitch = 100

params = ["userScript", x, y, z, startLeistung, pulse, repRate, PulseEnergy, hv,
        EnergyMode, TriggerMode, waitMs, pitch]
#queue = [[0,0],[1,0],[1,1],[1,2],[1,3],[0,1]]
#p = [[0,0],[4,2]]
#l = [[0,0,2,0],[2,0,2,3],[2,3,1,3],[1,3,1,2]]
#scriptConverter.doRasterfahrtIn(params, 5, 5)

queue, p, l = readGDS2txt.getCoordinates("test2.txt")
print(queue)
print(p)
print(l)
scriptConverter.createUserScript(params, queue, p, l)

#with open("twoDTest.txt", 'w') as f:
#    scriptConverter.twoDShoot(f, 0, 5, 0, 5)
