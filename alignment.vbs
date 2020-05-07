Option Explicit

dim x1, y1
dim corrAngle
dim dist

x1 = 39.290
y1 = -61.143
corrAngle = -2.864
dist = 73.602

' Available axis description ***************************************************
' x,y: Grid position [mm]
' c: Rotation position [deg]

' Move to (x1,y1), the left most alignment point. Script will rotate around that point to remove tilt.
' Then move dist to the right to right most alignment point. Check if its correct.

' Program start ***********************************************************

move x, x1
move y, y1
waituntilinpos x, y
wait 1000	'waituntilinpos does not always work apparently

move c, corrAngle
waituntilinpos c
wait 1000

moveRel x, dist
waituntilinpos x


