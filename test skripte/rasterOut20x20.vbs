Option Explicit

' Define all used variables ***************************************************

dim unit, startX, startY, startZ, startLeistung
dim xDistArray, yDistArray
dim pulse
dim i,j
dim pulseEnergyDist, HVVal, energyModeVal, triggerModeVal
dim waitMs
startX = 0.000
startY = 0.000
startZ = 0.000
startLeistung = -26.00
pulse = 1
pulseEnergyDist = 0
HVVal = 26
energyModeVal = 0
triggerModeVal = 0
waitMs = 100


' Available axis description ***************************************************
' x,y: Grid position [mm]
' z: Focus position [mm]
' Leistung: Reducer position [deg]
' Maske: Projection mask position [mm]


' Used subprocedures ***********************************************************

Sub setCompexproParams(energyModeVal, triggerModeVal, pulseEnergyVal, HVVal)
    compexpro.EnergyMode energyModeVal
    compexpro.TriggerMode triggerModeVal
    compexpro.PulseEnergy pulseEnergyVal
    'compexpro.HV HVVal
    compexpro.On
    compexpro.WaitUntilReady
End Sub

Sub moveAbs(xPos, yPos)
    move x, xPos
    move y, yPos
    waituntilinpos x,y
End Sub

Sub lineRelShootX(numShots, dist)
    for i=0 to numShots
        moveRel x, dist
        waituntilinpos x
        PSOPulse startShots, 1000000/20
    next
End Sub

Sub lineRelShootY(numShots, dist)
    for i=0 to numShots
        moveRel y, dist
        waituntilinpos y
        PSOPulse startShots, 1000000/20
    next
End Sub

Sub xyArrayShoot(numShots)
    for i=0 to numShots
        moveRel x, xArray(i)*unit
        moveRel y, yArray(i)*unit
        waituntilinpos x,y
        PSOPulse startShots, 1000000/20
    next
End Sub

Sub PSOPulse(nShots, fPulseWidth)
    If nShots < 1 Then Exit Sub
    Output A3200DOD3, 8, 1      ' Enable Trigger
    Output A3200DOD3, 9, 1      ' Enable Gate
    Output A3200DOD3, 10, 1     ' S1
    Output A3200DOD3, 11, 1     ' S2
	Dim strCmd, fTime
	fTime= Round(nShots*fPulseWidth/ 1000000, 3) + 0.1
	Echo "PSO Pulse " & nShots & ", Pulsewidth=" & fPulseWidth & " µs, Time=" & fTime & "s"
	strCmd= "PSOCONTROL Y RESET" & vbNewLine
	strCmd = strCmd & "PSOPULSE Y TIME " & Round(fPulseWidth, 0) & " " & Round(fPulseWidth/2, 0)  &" CYCLES " & nShots & vbNewLine
	strCmd = strCmd & "PSOCONTROL Y FIRE" & vbNewline
	strCmd = strCmd & "DWELL " & fTime & vbNewline
	echo strCmd
	A3200.Run strCmd
End Sub

' Program start ***********************************************************

setCompexproParams energyModeVal, triggerModeVal, pulseEnergyVal, HVVal

move x, startX
move y, startY
move z, startZ
move Leistung, startLeistung
waituntilinpos x, y, z, Leistung
wait 1000	' waituntilinpos does not always work

open shutter
wait waitMs
moveAbs 0.000, 0.000
PSOPulse pulse, 1000000/20.000

lineRelShootX 1,5.000
lineRelShootY 1,-5.000
lineRelShootX 2,-5.000
lineRelShootY 2,5.000
lineRelShootX 3,5.000
lineRelShootY 3,-5.000
lineRelShootX 4,-5.000
lineRelShootY 4,5.000
lineRelShootX 4,5.000
