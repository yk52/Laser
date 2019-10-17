#!/usr/bin/env python
from tkinter import *

canvasWidth = 400
canvasHeight = 400

def createGrid(canvas, lineDist):
    for x in range(lineDist, canvasWidth, lineDist):
        canvas.create_line(x, 0, x, canvasHeight, fill="#476042")
    for y in range(lineDist, canvasHeight, lineDist):
        canvas.create_line(0, y, canvasWidth, y, fill="#476042")

def insertBlank(rootFrame):
    Label(rootFrame, text=" ").pack()


# Creates dropdown options menue. optionsArray must contain string  
def dropDown(frame, optionsArray):
    stvar = StringVar()
    stvar.set(optionsArray[0])
    numOptions = len(optionsArray)
    if (numOptions == 4):
        option = OptionMenu(frame, stvar, optionsArray[0], optionsArray[1],
                optionsArray[2], optionsArray[3])
    if (numOptions == 3):
        option = OptionMenu(frame, stvar, optionsArray[0], optionsArray[1],
                optionsArray[2])
    if (numOptions == 2):
        option = OptionMenu(frame, stvar, optionsArray[0], optionsArray[1])

    return option

root = Tk()
root.title("Micromac Laser Ansteuerung")
c = Canvas(root, width=canvasWidth, height=canvasHeight)
c.grid(row=0, column=0, sticky="n")
createGrid(c,10)
frame = Frame(root)
frame.grid(row=0, column=1)
option = dropDown(frame, ["one", "two", "three"])
option.grid(row=0, column=1, sticky="nwe")
labelDropdown = Label(frame, text="Dropdown").grid(row=0, column=0, sticky="ne")
mainloop()

