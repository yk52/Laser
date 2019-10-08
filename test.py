#!/usr/bin/env python
"""
test script for scriptConverter
"""

import scriptConverter

with open("testSkript.txt", 'w') as f:
    scriptConverter.doRasterfahrtIn(f, 0.5, 0.5, 0.2, 4.4, 4.22)
