#!/usr/bin/env python

import ctypesgentest
from ctypes import *

header = """
struct foo
{
	int a;
	int b;
	int c;
};
"""

module, output = ctypesgentest.test(header)

struct_foo = module.struct_foo
assert struct_foo._fields_ == [("a", c_int), ("b", c_int), ("c", c_int)]

print "Tests OK."
