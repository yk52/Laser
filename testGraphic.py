#!/usr/bin/env python
"""
test script graphically
"""
import scriptConverter
from tkinter import *

def checkered(canvas, line_distance):
   # vertical lines at an interval of "line_distance" pixel
   for x in range(line_distance,canvas_width,line_distance):
      canvas.create_line(x, 0, x, canvas_height, fill="#476042")
   # horizontal lines at an interval of "line_distance" pixel
   for y in range(line_distance,canvas_height,line_distance):
      canvas.create_line(0, y, canvas_width, y, fill="#476042")


""" Get the coordinates %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
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
pitch = 20

params = ["OutTest", x, y, z, startLeistung, pulse, repRate, PulseEnergy, hv,
        EnergyMode, TriggerMode, waitMs, pitch]
queue = [[0,0],[1,0],[1,1],[1,2],[1,3],[0,1]]
p = [[0,0],[4,2]]
l = [[0,0,2,0],[2,0,2,3],[2,3,1,3],[1,3,1,2]]
scriptConverter.doRasterfahrtOut(params, 5, 5)
#scriptConverter.createUserScript(params, queue, p, l)

a,b,c,d = 40, 40, 580, 60


with open("twoDTest.txt", 'w') as f:
    testArray = scriptConverter.diagonalShoot(f, a, b, c, d)
print(testArray)


""" Show the lines %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

master = Tk()
canvas_width = 600
canvas_height = 600 
w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
w.pack()

checkered(w,20)

line = w.create_line(a, b, c, d)
w.pack()

for xy in testArray:
    line = w.create_oval(xy[0],xy[1],xy[0],xy[1], width = 5, fill='orange')

w.pack()
master.mainloop()
