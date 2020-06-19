Option Explicit

dim x1, y1
dim corrAngle
dim dist

x1 = 1.000
y1 = 1.000
corrAngle = 45.000
dist = 1.414

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


