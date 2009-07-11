#!/usr/bin/env python

import ctypesgentest
from ctypes import *
import math, sys

header = """
#include <math.h>
"""

if sys.platform == "linux2":
	module, output = ctypesgentest.test(header, libraries=["libm.so.6"], all_headers=True)
else:
	module, output = ctypesgentest.test(header, libraries=["libc"], all_headers=True)

assert module.sin(2) == math.sin(2)
assert module.sqrt(4) == 2

try:
	module.sin("foobar")
except ArgumentError:
	pass
else:
	raise Exception("ctypesgen thinks that it is reasonable to take the sin of a string.")

print "Tests OK."
