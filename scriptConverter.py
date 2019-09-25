#!/usr/bin/env python
"""
23/09/19
Take the path entered into the laser GUI and convert it into a visual basic script (.vbs) script
"""

import os

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

def readPath(grid):
	# get grid and turn into path
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
	
def createScript(fileName, initValues, coordinates):
	# output script made out of basic code blocks
	# Goal: Only one standard form with different values, but different path

	setParams(initValues)
	with open(fileName+".vbs", 'w') as vbs:
		vbs.write("Option Explicit\n\n")
		# First define all variables
		vbs.write("' Define all used variables ***************************************************\n\n")
		vbs.write("dim startX, startY, startZ, startLeistung\n")
		vbs.write("dim pulse, repRate, numShots\n")
		vbs.write("dim i,j\n")
		vbs.write("dim pulseEnergyVal, HVVal, energyModeVal, triggerModeVal\n")
		vbs.write("dim waitMs\n\n")
		vbs.write("startX = %.3f\n" %startX)
		vbs.write("startY = %.3f\n" %startY)
		vbs.write("startZ = %.3f\n" %startZ)
		vbs.write("startLeistung = %.3f\n" %startLeistung)
		vbs.write("pulse = %d\n" %pulse)
		vbs.write("repRate = %d\n" %repRate)
		vbs.write("numShots = %d\n" %numShots)
		vbs.write("pulseEnergyVal = %d\n" %pulseEnergy)
		vbs.write("HVVal = %d\n" %hv)
		vbs.write("energyModeVal = %d\n" %energyMode)
		vbs.write("triggerModeVal = %d\n" %triggerMode)
		vbs.write("waitMs = %d\n\n" %waitMs)
			
		# Second enter all used subprocedures and code main body
		with open("body.txt", 'r') as body:	
			for line in body:
				vbs.write(line)
				
		# Third enter movement and laser procedure
		arrayLen = len(coordinates)-1
		for i in range(0, arrayLen+1):
			vbs.write("\nmoveRel x, %f\n" %coordinates[i][0])
			vbs.write("moveRel y, %f\n" %coordinates[i][1])
			vbs.write("waituntilinpos x,y\n")
			vbs.write("PSOPulse pulse, 1000000/%f\n" %repRate)
		
		# Fourth enter what's left to say
		with open("end.txt", 'r') as body:	
			for line in body:
				vbs.write(line)
