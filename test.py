#!/usr/bin/env python
"""
test script for scriptConverter
"""

import scriptConverter

params = ["testRaster", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
scriptConverter.doRasterfahrtIn(params, 0.5, 0.5, 0.1)
