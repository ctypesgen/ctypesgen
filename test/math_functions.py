import ctypesgentest
from ctypes import *
import math

header = """
#include <math.h>
"""

module, output = ctypesgentest.test(header, libraries=["libc"], all_headers=True)

assert module.sin(2) == math.sin(2)
assert module.sqrt(4) == 2

try:
	module.sin("foobar")
except ArgumentError:
	pass
else:
	raise Exception, "ctypesgen thinks that it is reasonable to take the sin of a string."

print "Tests OK."