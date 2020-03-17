#!/usr/bin/env python3

import gdspy
import readGDS2txt

#q,p,l = readGDS2txt.getCoordinates("test2.txt")
#
#print(q)
#print(p)
#print(l)

gdsii = gdspy.GdsLibrary(infile='LH03_V10.45_170317.gds')
gdspy.LayoutViewer(gdsii)
