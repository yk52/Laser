#!/usr/bin/env python
"""
test script for scriptConverter
"""

import scriptConverter

params = ["testRaster", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 1]
queue = [[0,0],[1,0],[1,1],[1,2],[1,3],[0,1]]
p = [[0,0],[4,2]]
l = [[0,0,2,0],[2,0,2,3],[2,3,1,3],[1,3,1,2]]
#scriptConverter.doRasterfahrtIn(params, 0.5, 0.5, 0.1)
#scriptConverter.createUserScript(params, queue, p, l)

with open("twoDTest.txt", 'w') as f:
    scriptConverter.twoDShoot(f, 0, 5, 0, 5)
