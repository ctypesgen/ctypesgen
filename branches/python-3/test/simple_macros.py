#!/usr/bin/env python

import ctypesgentest
from ctypes import *

header = """
#define A 1
#define B(x,y) x+y
#define C(a,b,c) a?b:c
#define funny(x) "funny" #x
"""

module, output = ctypesgentest.test(header)

assert module.A==1
assert module.B(2,2)==4
assert module.C(True, 1,2)==1
assert module.C(False, 1,2)==2
assert module.funny("bunny") == "funnybunny"

print "Tests OK."
