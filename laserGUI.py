#!/usr/bin/env python
from tkinter import *

canvasWidth = 200
canvasHeight = 100

def createGrid(canvas, lineDist):
    for x in range(lineDist, canvasWidth, lineDist):
        canvas.create_line(x, 0, x, canvasHeight, fill="#476042")
    for y in range(lineDist, canvasHeight, lineDist):
        canvas.create_line(0, y, canvasWidth, y, fill="#476042")

master = Tk()
w = Canvas(master, width=canvasWidth, height=canvasHeight)
w.pack()
createGrid(w,10)
mainloop()

