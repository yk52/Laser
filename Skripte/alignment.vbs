Option Explicit

dim x1, y1
dim corrAngle
dim dist

x1 = 32.883
y1 = -65.691
corrAngle = 2.483
dist = 74.001

' Available axis description ********************************************
'*************************************************************************
' x,y: Grid position [mm]
' c: Rotation position [deg]

' Move to (x1,y1), the left most alignment point.
' Script will rotate around that point to remove tilt.
'*************************************************************************
'*************************************************************************


' Program start ******

move x, x1
move y, y1
waituntilinpos x, y
wait 1000	'waituntilinpos does not always work apparently

move c, corrAngle
waituntilinpos c
wait 1000


