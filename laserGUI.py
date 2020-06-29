#!/usr/bin/env python
""" 
Creates GUI for Laser control in order to access alignment.py and
scriptConverter.py 
Script is created by setting together basic blocks of code which can be
found under the folder "textmodule"
"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import traceback
import alignment
import scriptConverter


entries = {}
switchVariables = {}
switchCounter = 0


"""
input:  rootFrame: Parent frame object
        fields:    Descriptions of Entry boxes (Array of strings.
                   e.g. ["x", "y", "z"]) 

effect: Creates entry boxes. Labels are the strings in "fields".
"""
def makeformText(rootFrame, fields):
    global entries
    if (len(fields) > 1):
        for field in fields:
            row = tk.Frame(rootFrame)
            lab = tk.Label(row, width=13, text=field, anchor='w')
            lab.pack(side="left")
            ent = tk.Entry(row)
            row.pack(side="top", fill="x", padx=5, pady=5)
            ent.pack(side="right",expand="yes",fill="x")
            entries[field] = ent


"""
input:  rootFrame: Parent frame object
        fields:    Descriptions of buttons (Array of strings.
                   e.g. ["x", "y", "z"])
        btn1:      Name of left button 
        btn2:      Name of right button 
        
effect: Creates 2 buttons next to each other with values btn1 and btn2.
        Labels are the strings in "fields".
"""
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
        switchVariables[switchVar] = tk.StringVar(value=btnVal1)
        button1 = tk.Radiobutton(row, text=btn1, padx = 10,
                variable=switchVariables[switchVar], indicatoron=False,
                value=btnVal1, width=6, bg='gray90')
        button2 = tk.Radiobutton(row, text=btn2, padx = 10,
                variable=switchVariables[switchVar], indicatoron=False,
                value=btnVal2, width=6, bg='gray90')
        lab = tk.Label(row, width=13, text=field, anchor='w')
        lab.pack(side="left")
        row.pack(side="top", fill="x", padx=5, pady=5)
        button1.pack(side="left")
        tk.Label(row, text=" ").pack(side="left")   # add space btw buttons
        button2.pack(side="left")
        entries[field] = switchVariables[switchVar]
        switchCounter += 1 
    return len(entries)


"""
input:  rootFrame: Parent frame object
        
effect: Insert blank line to rootFrame
"""
def insertBlank(rootFrame):
    tk.Label(rootFrame, text=" ").pack()

"""
input:  None 
        
effect: Show last line of error if one occurs in messagebox
"""
def showError(self, *args):
    err = traceback.format_exception(*args)
    messagebox.showerror('Error occured. Press [Get Help] for further assistance.'
            , err[-2:])


"""
input:  None 
        
effect: Show that scipt conversion was succesful
"""
def showSuccess():
    successMsg = "Script conversion successful"
    messagebox.showinfo("Info", successMsg)

"""
input:  None 
        
effect: Show help message and open LaserGUIHelp.pdf in folder LaserHelp
"""
def showHelp():
    helpMsg = "For a detailed documentation, kindly refer to the "+\
    "LaserHelp.pdf file in the LaserGUIHelp folder.\n"+\
    "It will open automatically after you close this window.\n"+\
    "If you get an error, the file has been deleted, or misplaced. Ohwee.\n"+\
    "\nContact kakuy@tf.uni-freiburg.de for further assistance."
    messagebox.showinfo("Help", helpMsg)
    os.system("start LaserHelp/LaserGUIHelp.pdf")

"""
input:  root:   parent frame object   
        
effect: Create Layout of GUI and return interactive user entries, as well
        as parent frames for startBtn1 and startBtn2
"""
def createLayout(root):
    global entries

    # Alignment
    alignFrame = tk.Frame(root, relief="sunken", borderwidth=5)
    alignFrame.pack(side='left', anchor='n', padx=10, pady=10)
    tk.Label(alignFrame, bg='LavenderBlush3', text="Step 1) Tilt alignment", font=25).pack(fill='x')
    tk.Label(alignFrame, text="Use camera coordinates", font=18).pack(fill='x')
    leftRightFrame = tk.Frame(alignFrame)
    leftRightFrame.pack(pady=5)
    leftAlignFrame = tk.Frame(leftRightFrame, borderwidth=3, relief="groove")
    rightAlignFrame = tk.Frame(leftRightFrame, borderwidth=3, relief="groove")
    tk.Label(leftAlignFrame, text="Left alignment point [mm]", bg='LavenderBlush2').pack(fill='x')
    tk.Label(rightAlignFrame, text="Right alignment point [mm]", bg='LavenderBlush2').pack(fill='x')
    makeformText(leftAlignFrame, ["x1", "y1"])
    makeformText(rightAlignFrame, ["x2", "y2"])
    leftAlignFrame.pack(padx=10)
    rightAlignFrame.pack(padx=10)


    # Laser settings
    rasterFrame = tk.Frame(root, relief="sunken", borderwidth=5)
    rasterFrame.pack(pady=10)
    tk.Label(rasterFrame, text="Step 2)  Rasterfahrt", bg='honeydew3', font=50).pack(fill='x')

    # Left side coordinate frame start
    coordinateFrame = tk.Frame(rasterFrame)
    coordinateFrame.pack(side='left', anchor='n', padx=10, pady=5)

    alignDesignFrame = tk.Frame(coordinateFrame, relief="groove", borderwidth=3)
    alignDesignFrame.pack()
    tk.Label(alignDesignFrame, text="Origin in design [mm]", bg='honeydew2').pack(fill='x')
    makeformText(alignDesignFrame, ['x0D', 'y0D'])

    shootDesignFrame = tk.Frame(coordinateFrame, relief="groove", borderwidth=3)
    shootDesignFrame.pack()
    tk.Label(shootDesignFrame, text="First shooting point in\
 design [mm]", bg='honeydew2').pack(fill='x')
    makeformText(shootDesignFrame, ['xD', 'yD'])

    shotFrame = tk.Frame(coordinateFrame, relief="groove", borderwidth=3)
    shotFrame.pack()
    tk.Label(shotFrame, text="Origin in laser coordinates [mm]", bg='honeydew2').pack(fill='x')
    makeformText(shotFrame, ['x0', 'y0'])

    # Right Misc frame start
    miscFrame = tk.Frame(rasterFrame)
    miscFrame.pack(side="right", anchor='n', pady=5)
    sub = tk.Frame(miscFrame, relief="groove", borderwidth=3)
    sub.pack()
    makeformButton(sub, ['Direction'], btn1='Inwards', btn2='Outwards')
    makeformText(sub, ['Script name', 'pitch [mm]', 'startZ [mm]', 'Square \
size [mm]'])

    extraFrame = collapseFrame(sub, text='More Settings...',
            relief="raised")
    extraFrame.pack(padx=3, pady=3, fill='x')
    f2 = ['StartLeistung', 'PulseEnergy', 'EnergyMode',\
            'TriggerMode', 'waitMs', 'Pulse', 'repRate', 'Overlap']
    makeformText(extraFrame.subFrame, f2)

    return alignFrame, miscFrame, entries

"""
input:  inputs: Dictionary with user inputs
        
effect: Read user inputs for the alignment part and create alignment script in
        "Skripte" folder. Success window pops up after creation.
"""
def fetchAlign(inputs):
    x1 = float(inputs['x1'].get())
    y1 = float(inputs['y1'].get())
    x2 = float(inputs['x2'].get())
    y2 = float(inputs['y2'].get())

    p1 = (x1, y1)
    p2 = (x2, y2)
    alignment.removeTilt(p2,p1)
    showSuccess()

"""
input:  inputs: Dictionary with user inputs
        
effect: Read user inputs for the Rasterfahrt part and create script in 
        "Skripte" folder. Success window pops up after creation.

NOTE:   COORDINATE SYSTEM:  X left: -, right: +
                            Y up: -, down: +
"""
def fetchLaser(inputs):
    params = {}

    # Process inputs and handle errors
    dataNameError = "Invalid data name input.\n"+\
    "\nValid input example:\nFor [foo.vbs], enter [foo]."

    buttonError = "Please be sure to choose one of the given options."
    mandatoryError ="Please check if you've filled all necessary boxes."

    filename = inputs['Script name'].get()
    xD = float(inputs['xD'].get())
    yD = float(inputs['yD'].get())
    x0D = float(inputs['x0D'].get())
    y0D = float(inputs['y0D'].get())
    x0 = float(inputs['x0'].get())
    y0 = float(inputs['y0'].get())
    startZ = float(inputs['startZ [mm]'].get())

    moveXRel = xD - x0D    
    moveYRel = yD - y0D

    startX =  x0 + moveXRel
    startY = y0 + moveYRel
    origin = (x0, y0)

    size = float(inputs['Square size [mm]'].get())
    pitch = float(inputs['pitch [mm]'].get())

    if (pitch > size):
        msg = "Pitch is larger than size"
        messagebox.showerror("Boundary error", msg)
        return

    if ((startX + size) > 150 or ((startY - size) < -298)):
        msg = "Movement would exceed Laser boundaries.\n\
Please choose different starting point or decrease size.\n\
Range of the laser: x=[0,150], y=[0,-298]"
        messagebox.showerror("Boundary error", msg)
        return

    defaults = {'StartLeistung':-26, 'PulseEnergy':220, 'EnergyMode':0,\
            'TriggerMode':0, 'waitMs':100, 'Pulse':1, 'repRate':20,\
            'Overlap':0}
    
    for key in defaults:
        inp = inputs[key].get()
        if (inp == ''):
            inp = float(defaults[key])
        else:
            inp = float(inp)

        defaults[key] = inp    

    StartLeistung = defaults['StartLeistung']
    PulseEnergy = defaults['PulseEnergy']
    EnergyMode = defaults['EnergyMode']
    TriggerMode = defaults['TriggerMode']
    waitMs = defaults['waitMs']
    Pulse = defaults['Pulse']
    repRate = defaults['repRate']
    Overlap = defaults['Overlap']

    pitch -= Overlap
    params = {"origin":origin, "overlap":Overlap, "fileName":filename, \
            "startX":startX, "startY":startY, "startZ":startZ,\
            "startLeistung":StartLeistung, "pulse":Pulse, "repRate":repRate,\
            "pulseEnergy":PulseEnergy, \
            "energyMode":EnergyMode, "triggerMode":TriggerMode,\
            "waitMs":waitMs, "pitch":pitch, "size":size}

    if (inputs['Direction'].get() == 'Inwards'):
        scriptConverter.doRasterfahrtIn(params)
    else:
        scriptConverter.doRasterfahrtOut(params)

    showSuccess()



"""
input:  tk.Frame: parent frame object
        
effect: Create collapsing frame with radio buttons. Default is the collapsed state.
        By clicking yes, the frame appears.
"""
class collapseFrame(tk.Frame):
    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)
        self.show = tk.IntVar()
        self.show.set(0)
        self.titleFrame = ttk.Frame(self)
        self.titleFrame.pack(fill="x", expand=1, padx=3, pady=5)

        tk.Label(self.titleFrame, width=13, anchor='w',
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
    root.title("Laser Control")
    root.resizable(False, False)
    frame = tk.Frame(root)
    frame.pack()

    # Create whole layout if user interaction
    alignFrame, miscFrame, ents = createLayout(frame)

    # Create alignment button
    buttonFrame1 = tk.Frame(alignFrame)
    buttonFrame1.pack(anchor='se')
    startBtn1 = tk.Button(buttonFrame1, text="Create alignment script", \
            bg="Gray70", command=(lambda e=ents: fetchAlign(e)))
    startBtn1.pack(anchor='se', padx=10, pady=5)

    # Create Rasterfahrt button
    buttonFrame2 = tk.Frame(miscFrame)
    buttonFrame2.pack(anchor='se')
    startBtn2 = tk.Button(buttonFrame2, text="Create Rasterfahrt script", \
            bg="Gray70", command=(lambda e=ents: fetchLaser(e)))
    startBtn2.pack(anchor='se',  padx=10, pady=5)

    # Create Help button
    helpFrame = tk.Frame(root)
    helpFrame.pack(side='right')
    helpBtn = tk.Button(helpFrame, text="Get help", bg="Gray64", \
            command=(lambda:showHelp()))
    helpBtn.pack(side="right", fill="x", padx=7, pady=5)

    tk.Tk.report_callback_exception = showError
    root.mainloop()



if __name__ == '__main__':
    main()
