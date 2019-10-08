#!/usr/bin/env python
"""
test script for scriptConverter
"""

import scriptConverter

with open("testSkript.txt", 'w') as f:
    scriptConverter.doRasterfahrtOut(f, 1, 1, 1, 4.4, 4.22)
