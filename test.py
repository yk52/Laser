#!/usr/bin/env python
"""
test script for scriptConverter
"""

import scriptConverter

with open("testSkript.txt", 'w') as f:
    scriptConverter.doRasterfahrtOut(f, 0.5, 0.5, 0.1, 0, 0)
