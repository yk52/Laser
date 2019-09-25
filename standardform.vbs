Option Explicit

dim startX, startY, startZ, startLeistung
dim pulse, repRate, numShots
dim i,j
dim pulseEnergyVal, HVVal, energyModeVal, triggerModeVal
dim waitMs

startX = float
startY = float
startZ = float
startLeistung = float
pulse = int
repRate = int
numShots = int
pulseEnergyVal = int
HVVal = int
energyModeVal = int
triggerModeVal = int
waitMs = int

' Available axis description ***************************************************
' x,y: Grid position [mm]
' z: focus position [mm]
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

setCompexproParams energyModeVal, triggerModeVal, pulseEnergyVal, HVVal

move x, startX
move y, startY
move z, startZ
move Leistung, startLeistung
waituntilinpos x, y, z, Leistung
wait 1000	' waituntilinpos does not always work

open shutter
wait waitMs
