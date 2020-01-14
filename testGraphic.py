#!/usr/bin/env python
"""
test script graphically
"""
import scriptConverter
import readGDS2txt
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
x = 50
y = 50
z = 50
startLeistung = -26
pulse = 1
repRate = 20 
PulseEnergy = 220
hv = 26
EnergyMode = 0
TriggerMode = 0
waitMs = 100
pitch = 50

params = ["trying", x, y, z, startLeistung, pulse, repRate, PulseEnergy, hv,
        EnergyMode, TriggerMode, waitMs, pitch]
#queue = [[0,0],[1,0],[1,1],[1,2],[1,3],[0,1]]
#p = [[0,0],[4,2]]
#l = [[0,0,2,0],[2,0,2,3],[2,3,1,3],[1,3,1,2]]
# testArray = scriptConverter.doRasterfahrtIn(params, 5000, 5000)
#scriptConverter.createUserScript(params, queue, p, l)

#x0,y0, x1,y1
a,b,c,d = 20, 20, 20, 540


queue, p, l = readGDS2txt.getCoordinates("test.txt")
testArray = scriptConverter.createUserScript(params, queue, p, l)

""" Show the lines %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

master = Tk()
canvas_width = 1000
canvas_height = 1000
w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
w.pack()

checkered(w,pitch)
print(l)

w.create_oval(500,500,500,500, width = 10, fill='orange')
w.pack()

# test diagonal shoot
for i in range(len(queue)):
    if (queue[i][0] == 1):
        idx = queue[i][1]
        line = w.create_line(l[idx][0]+500,500-l[idx][1],l[idx][2]+500,500-l[idx][3], width = 2)

w.pack()

print(testArray)
for xy in testArray:
    #positions of shots
    point = w.create_oval(xy[0]+500,500-xy[1],xy[0]+500,500-xy[1], width = 5, fill='orange')

w.pack()
master.mainloop()
