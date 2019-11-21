Option Explicit

' Define all used variables ***************************************************

dim startX, startY, startZ, startLeistung
dim pulse
dim i,j
dim pulseEnergyDist, HVVal, energyModeVal, triggerModeVal
dim waitMs

startX = 10.000
startY = 10.000
startZ = 10.000
startLeistung = -26.000
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


Sub PSOPulse(nShots, fPulseWidth)
    If nShots < 1 Then Exit Sub
    Output A3200DOD3, 8, 1      ' Enable Trigger
    Output A3200DOD3, 9, 1      ' Enable Gate
    Output A3200DOD3, 10, 1     ' S1
    Output A3200DOD3, 11, 1     ' S2
	Dim strCmd, fTime
	fTime= Round(nShots*fPulseWidth/ 1000000, 3) + 0.1
	Echo "PSO Pulse " & nShots & ", Pulsewidth=" & fPulseWidth & " �s, Time=" & fTime & "s"
	strCmd= "PSOCONTROL Y RESET" & vbNewLine
	strCmd = strCmd & "PSOPULSE Y TIME " & Round(fPulseWidth, 0) & " " & Round(fPulseWidth/2, 0)  &" CYCLES " & nShots & vbNewLine
	strCmd = strCmd & "PSOCONTROL Y FIRE" & vbNewline
	strCmd = strCmd & "DWELL " & fTime & vbNewline
	echo strCmd
	A3200.Run strCmd
End Sub

' Program start ***********************************************************

setCompexproParams energyMode, triggerMode, startLeistung, HV

move x, startX
move y, startY
move z, startZ
move Leistung, startLeistung
waituntilinpos x, y, z, Leistung
wait 1000	' waituntilinpos does not always work

open shutter
wait waitMs

move x, 10.000000
move y, 10.000000
waituntilinpos x,y
wait waitMs

moveRel x, 1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, 1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, 1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, 1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, 1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, 0.000000
moveRel y, 1.000000
waituntilinpos x,y
wait waitMs

moveRel x, 0.000000
moveRel y, 1.000000
waituntilinpos x,y
wait waitMs

moveRel x, 0.000000
moveRel y, 1.000000
waituntilinpos x,y
wait waitMs

moveRel x, 0.000000
moveRel y, 1.000000
waituntilinpos x,y
wait waitMs

moveRel x, 0.000000
moveRel y, 1.000000
waituntilinpos x,y
wait waitMs

moveRel x, -1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, -1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, -1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, -1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, -1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, 0.000000
moveRel y, -1.000000
waituntilinpos x,y
wait waitMs

moveRel x, 0.000000
moveRel y, -1.000000
waituntilinpos x,y
wait waitMs

moveRel x, 0.000000
moveRel y, -1.000000
waituntilinpos x,y
wait waitMs

moveRel x, 0.000000
moveRel y, -1.000000
waituntilinpos x,y
wait waitMs

moveRel x, 1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, 1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, 1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, 1.000000
moveRel y, 0.000000
waituntilinpos x,y
wait waitMs

moveRel x, 0.000000
moveRel y, 1.000000
waituntilinpos x,y
wait waitMs
PSOPulse pulse, 1000000/20.000000



