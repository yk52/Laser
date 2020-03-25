Option Explicit

dim x1, y1
dim corrAngle
dim dist

x1 = -20000.000
y1 = 2500.000
corrAngle = 11.768
dist = 61288.253

' Available axis description ***************************************************
' x,y: Grid position [mm]
' c: Rotation position [deg]

' Move to (x1,y1), the left most alignment point. Script will rotate around that point to remove tilt.
' Then move dist to the right to right most alignment point. Check if its correct.

' Program start ***********************************************************

' These 2 needed if I only use camera and axis?
compexpro.On
compexpro.WaitUntilReady

move x, x1
move y, y1
waituntilinpos x, y
wait 1000	'waituntilinpos does not always work apparently

move c, corrAngle
waituntilinpos c
wait 1000

moveRel x, dist
waituntilinpos x


