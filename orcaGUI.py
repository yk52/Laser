#!/usr/bin/env python
""" 
Needed variables:
startx,starty,startz,startLeistung
compexpro: HV, Triggermode, wait

"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import traceback
import numpy as np


entries = []
switchVariables = {}
switchCounter = 0


def makeformText(rootFrame, fields):
    global entries
    for field in fields:
        row = tk.Frame(rootFrame)
        lab = tk.Label(row, width=25, text=field, anchor='w')
        lab.pack(side="left")
        ent = tk.Entry(row)
        row.pack(side="top", fill="x", padx=5, pady=5)
        ent.pack(side="right",expand="yes",fill="x")
        entries.append((field,ent))


def makeformButton(rootFrame, fields, btn1='yes', btn2='no'):
    global entries
    global switchCounter
    btnVal1 = btn1
    btnVal2 = btn2
    if (btn1 == 'yes'):
        btnVal1 = 'y'
        btnVal2 = 'n'
    for field in fields:
        row = tk.Frame(rootFrame)
        switchVar = "switchVar%d" %switchCounter
        switchVariables[switchVar] = tk.StringVar(value="none")
        button1 = tk.Radiobutton(row, text=btn1, padx = 5,
                variable=switchVariables[switchVar], indicatoron=False,
                value=btnVal1, width=5)
        button2 = tk.Radiobutton(row, text=btn2, padx = 5,
                variable=switchVariables[switchVar], indicatoron=False,
                value=btnVal2, width=5)
        lab = tk.Label(row, width=25, text=field, anchor='w')
        lab.pack(side="left")
        row.pack(side="top", fill="x", padx=5, pady=5)
        button1.pack(side="left")
        button2.pack(side="left")
        entries.append((field,switchVariables[switchVar]))
        switchCounter += 1 
    return len(entries)


def insertBlank(rootFrame):
    tk.Label(rootFrame, text=" ").pack()


def createLayout(root, dataProcFrame, visFrame, polFrame):
    root.title("Script Converter for Laser Control")
    tk.Label(root, text="Laser path settings", font=25).pack()
    insertBlank(root)
    makeformText(root, ['Script name'])
    f1 = ['X start', 'Y start', 'Z start', 'Pitch [mm]', 'Power', 'Pulse', 'repRate',\
            'Pulse Energy', 'waitMs']
    makeformText(root, f1)

    dataProcFrame.pack(padx=5, pady=5, fill="x", anchor="n")
    makeformText(dataProcFrame.subFrame, ['Average over how many files?'])
    makeformButton(dataProcFrame.subFrame, ['Save whole file as .csv?'])
    makeformText(dataProcFrame.subFrame, ['Export single line?'])

    return entries


def fetch(inputs, d, v, p):
    userInputs = []

    for entry in inputs:
        singleInput = entry[1].get()
        userInputs.append(singleInput)
        
    processEntries(userInputs, processData, visualize, polar)   

def processEntries(inputs, processData, visualize, polar):
    # Process inputs and handle errors
    dataNameError = "Invalid data name input.\n"+\
    "\nValid input example:\nFor [foo_1.txt], enter [foo].\n"+\
    "\nCheck if the data files are named the following way:\n"+\
    "foo_{1...n}.txt or .npy"

    buttonError = "Please be sure to choose one of the given options."
    mandatoryError ="Please check all mandatory boxes and inputs with *."

    # Check if all mandatory 
    for i in range(8):
        if inputs[i] == ('none' or ''):
            messagebox.showerror("Mandatory inputs missing", mandatoryError)
            return

    i = 0
    dataName = inputs[i]
    if (len(dataName) >= 5):
        if (dataName[-4:]==".npy") or (dataName[-4:]==".txt") or \
            (dataName[-2]=="_"):
            messagebox.showerror("Data Name Error", dataNameError)
    # It's stupid that there is no i++ in python
    i += 1
    dataType = inputs[i]
    i += 1
    vSize = int(inputs[i])
    i += 1
    hSize = int(inputs[i])
    i += 1
    start = int(inputs[i])
    i += 1
    stop = int(inputs[i])
    i += 1
    maxValKnown = inputs[i]
    if (processData == 0):
        i += 3
    else:    
        i += 1
        avrgAmount = inputs[i]
        if (avrgAmount == ''):
            avrgAmount = 1
        else:
            avrgAmount = int(avrgAmount)
        i += 1
        csv = inputs[i]
        if (csv == 'none'):
            messagebox.showerror("Data processing error", buttonError)
        i += 1
        if (inputs[i] == ''):
            singleLine = -1
        else:    
            singleLine = int(inputs[i])
    if (visualize == 1):
        for j in range(12, 15):
            if inputs[i] == ('none'):
                messagebox.showerror("Visualization error", buttonError)
        i += 1
        heatmap = inputs[i]
        i += 1    # Highlight the halfMax value points to calculate distance
        highlight = inputs[i] 
        i += 1
        if (polar == 1):
            savePolarPng = inputs[i]
            i += 1    
            savePolarCsv = inputs[i]
            i += 1    
            dist = float(inputs[i])
            i += 1
            shiftDeg = inputs[i]
            if (shiftDeg == ''):
                shiftDeg = 0
            else:
                shiftDeg = int(shiftDeg)


    depth = stop - start + 1




def showError(self, *args):
    err = traceback.format_exception(*args)
    messagebox.showerror('Error occured', err[-1])


def showHelp():
    helpMsg = "For a detailed documentation, kindly refer to the "+\
    "README_BEAMAGEANALYZER.pdf file.\n"+\
    "(C:/Users/Beam/Desktop/Beam analyzer/README_BEAMAGE.txt)\n"+\
    "\nContact kakuy@tf.uni-freiburg.de for further assistance."
    messagebox.showinfo("Help", helpMsg)

class collapseFrame(tk.Frame):
    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)
        self.show = tk.IntVar()
        self.show.set(0)
        self.titleFrame = ttk.Frame(self)
        self.titleFrame.pack(fill="x", expand=1, padx=5, pady=5)

        tk.Label(self.titleFrame, width=25, anchor='w',
                text=text).pack(side="left")
        self.appearButton = ttk.Radiobutton(self.titleFrame, width=5, text="yes",
                command=self.toggle, value=1, variable=self.show)
        self.appearButton.pack(side="left")
        self.collapseButton = ttk.Radiobutton(self.titleFrame, width=5,
                text="no",
                command=self.toggle, value = 0, variable=self.show)
        self.collapseButton.pack(side="left")

        self.subFrame = tk.Frame(self, relief="groove",
                borderwidth=5)


    def toggle(self):
        if bool(self.show.get()):
            self.subFrame.pack(fill="x", expand=1)
        else:
            self.subFrame.forget()




def main():
    root = tk.Tk()
    dataFrame = collapseFrame(root, text = '1) Data processing required?*',
            relief="raised")
    visFrame = collapseFrame(root, text = '2) Visualization required?*',
            relief="raised")
    polFrame = collapseFrame(visFrame.subFrame, text = 'Polar plot?',
            relief="raised")
    ents = createLayout(root, dataFrame, visFrame, polFrame)
    insertBlank(root)
    quitBtn = tk.Button(root, text="Quit", bg="Gray64", command=(lambda:
        root.destroy()))
    quitBtn.pack(side="right", fill="x", padx=5, pady=5)

    startBtn = tk.Button(root, text="Start", bg="Gray64",command=(lambda e=ents,
        d=dataFrame, v=visFrame, p=polFrame: fetch(e,d,v,p)))

                
    startBtn.pack(side="right", fill="x", padx=7, pady=5)

    helpBtn = tk.Button(root, text="Get Help", bg="Gray64",command=(lambda:
        showHelp()))
    helpBtn.pack(side="right", fill="x", padx=5, pady=5)
    tk.Tk.report_callback_exception = showError
    root.mainloop()



if __name__ == '__main__':
    main()
