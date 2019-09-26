#!/usr/bin/env python
"""
23/09/19
Take the path entered into the laser GUI and convert it into a visual basic script (.vbs) script
"""

import os
import math
#import pyximport; pyximport.install()

# global variables
startX = 0
startY = 0
startZ = 0
startLeistung = 0
pulse = 0
repRate = 0
numShots = 0
pulseEnergy = 0
hv = 0
energyMode = 0
triggerMode = 0
waitMs = 0
rasterfahrt = 0
pitchArray = 0

def readGrid(grid):
        # get grid and turn into 2 arrays: start and stop
	return coordinates
	

def setParams(array):
	i = 0
	startX = array[i]
	i += 1
	startY = array[i]
	i += 1
	startZ = array[i]
	i += 1
	startLeistung = array[i]
	i += 1
	pulse = array[i]
	i += 1
	repRate = array[i]
	i += 1
	numShots = array[i]
	i += 1
	pulseEnergy = array[i]
	i += 1
	hv = array[i]
	i += 1
	energyMode = array[i]
	i += 1
	triggerMode = array[i]
	i += 1
	waitMs = array[i]
	
def defineVars():
	vbs.write("' Define all used variables ***************************************************\n\n")
	vbs.write("dim startX, startY, startZ, startLeistung\n")
	vbs.write("dim pulse, repRate, numShots\n")
	vbs.write("dim i,j\n")
	vbs.write("dim pulseEnergyDist, HVVal, energyModeVal, triggerModeVal\n")
	vbs.write("dim waitMs\n\n")
	vbs.write("startX = %.3f\n" %startX)
	vbs.write("startY = %.3f\n" %startY)
	vbs.write("startZ = %.3f\n" %startZ)
	vbs.write("startLeistung = %.3f\n" %startLeistung)
	vbs.write("pulse = %d\n" %pulse)
	vbs.write("repRate = %d\n" %repRate)
	vbs.write("numShots = %d\n" %numShots)
	vbs.write("pulseEnergyDist = %d\n" %pulseEnergy)
	vbs.write("HVVal = %d\n" %hv)
	vbs.write("energyModeVal = %d\n" %energyMode)
	vbs.write("triggerModeVal = %d\n" %triggerMode)
	vbs.write("waitMs = %d\n\n" %waitMs)
	
def moveRel(xDist, yDist):
	vbs.write("\nmoveRel x, %f\n" %xDist)
	vbs.write("moveRel y, %f\n" %yDist)
	vbs.write("waituntilinpos x,y\n")
	vbs.write("wait waitMs\n")

def moveAbs(xPos, yPos):
	vbs.write("\nmove x, %f\n" %xPos)
	vbs.write("move y, %f\n" %yPos)
	vbs.write("waituntilinpos x,y\n")
	vbs.write("wait waitMs\n")
        

"""
move into certain direction. 0=up, 1=right, 2=down, 3=left
down and right: +
up and left: -
"""
def moveDir(direction, dist):
        if direction == 0:      # up
                moveRel(0, -1*dist)
        elif direction == 1:      # right
                moveRel(dist, 0)
        elif direction == 2:      # down
                moveRel(0, dist)
        elif direction == 3:      # left
                moveRel(-1*dist, 0)
	

def shoot():
	vbs.write("PSOPulse pulse, 1000000/%f\n" %repRate)

def moveAndShootRel(xDist, yDist):
        moveRel(xDist, yDist)
	shoot()
	
def diagonalShoot(x0, x1, y0, y1, pitch):
	# TODO implement diagonal later. continue with for loop
	deltaX = x1 - x0
	deltaY = y1 - y0
	dist = math.sqrt(pow(deltaX,2)+pow(deltaY,2))
	numShots = dist / pitch
	
def lineRelShoot(direction, dist, pitch):
	# Starting position not shot automatically
        # 0 = start, 1 = stop
	numShots = dist / pitch
	for i in range(numShots):
                moveDir(direction, pitch)
                shoot()

def lineShoot(x0, x1, y0, y1, pitch):
	# Starting position not shot automatically
        # 0 = start, 1 = stop
	deltaX = x1 - x0
	deltaY = y1 - y0
	numShots = (deltaX + deltaY) / pitch	# Because either deltaX or Y is 0
	for i in range(numShots):
		moveAndShootRel(deltaX, deltaY)


"""	
Von Auﬂen nach Innen.
Bei auﬂen nach innen muss der Startpunkt immer links oben sein
dir = 0,1,2,3: Up, Right, Down, Left
!!! sizeX und sizeY m¸ssen Vielfaches von pitch sein!
"""

def doRasterfahrtIn(sizeX, sizeY, pitch, x0, y0):
	# TODO debug
	direction = 1
        lenX = sizeX
        lenY = sizeY
        moveAbs(x0, y0)
        shoot()     # first shot
        lineRelShoot(direction, lenX, pitch)   # first line to the right

        while(lenY >= pitch or lenX >= pitch):
                direction = (direction + 1) % 4
                if (lenY >= pitch):
                        lineRelShoot(direction, lenY, pitch)
                direction = (direction + 1) % 4
                if (lenX >= pitch): 
                        lineRelShoot(direction, lenX, pitch)
                lenY -= pitch
                lenX -= pitch


"""
Von Innen nach auﬂen. Geht nur vom Zentrum aus.
"""
def doRasterfahrtOut(sizeX, sizeY, pitch, x0, y0):
	# TODO Debug
        direction = 0
        lenX = 0
        lenY = 0

        moveAbs(x0, y0)
        shoot()     # first shot

        while (lenX <= sizeX or lenY <= sizeY):
                lenX += pitch
                lenY += pitch
                direction = (direction + 1) % 4
                if (lenX <= sizeX):
                        lineRelShoot(direction, lenX)
                else:
                        lineRelShoot(direction, lenX - pitch)
                direction = (direction + 1) % 4
                if (lenY <= sizeY):
                        lineRelShoot(direction, lenY)
                else:
                        lineRelShoot(direction, lenY - pitch)

	

def createScript(fileName, initValues, coordinates):
	# output script made out of basic code blocks
	# Goal: Only one standard form with different values, but different path

	setParams(initValues)
	with open(fileName+".vbs", 'w') as vbs:
		vbs.write("Option Explicit\n\n")
		# First define all variables
		defineVars()
			
		# Second enter all used subprocedures and code main body
		with open("body.txt", 'r') as body:	
			for line in body:
				vbs.write(line)
				
		# Third enter movement and laser procedure
		arrayLen = len(coordinates)-1
		for i in range(0, arrayLen+1):
			moveAndShootRel(coordinates[i][0], coordinates[i][1])
		
		# Fourth enter what's left to say
		with open("end.txt", 'r') as body:	
			for line in body:
				vbs.write(line)
