#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Simple test suite using unittest.
By clach04 (Chris Clark).

Calling:

    python test/testsuite.py 

or
    cd test
    ./testsuite.py 

Could use any unitest compatible test runner (nose, etc.)

Aims to test for regressions. Where possible use stdlib to
avoid the need to compile C code.

Known to run clean with:
  * 32bit Linux (python 2.5.2, 2.6)
  * 32bit Windows XP (python 2.4, 2.5, 2.6.1)
"""

import sys
import os
import ctypes
import math
import unittest
import logging

test_directory = os.path.abspath(os.path.dirname(__file__))
sys.path.append(test_directory)
sys.path.append(os.path.join(test_directory, '..'))

import ctypesgentest  # TODO consider moving test() from ctypesgentest into this module


class StdlibTest(unittest.TestCase):
    
    def setUp(self):
        """NOTE this is called once for each test* method
        (it is not called once per class).
        FIXME This is slightly inefficient as it is called *way* more times than it needs to be.
        """
        header_str = '#include <stdlib.h>\n'
        if sys.platform == "win32":
            # pick something from %windir%\system32\msvc*dll that include stdlib
            libraries = ["msvcrt.dll"]
            libraries = ["msvcrt"]
        elif sys.platform.startswith("linux"):
            libraries = ["libc.so.6"]
        else:
            libraries = ["libc"]
        self.module, output = ctypesgentest.test(header_str, libraries=libraries, all_headers=True)

    def tearDown(self):
        del self.module
        ctypesgentest.cleanup()

    def test_getenv_returns_string(self):
        """Issue 8 - Regression for crash with 64 bit and bad strings on 32 bit.
        See http://code.google.com/p/ctypesgen/issues/detail?id=8
        Test that we get a valid (non-NULL, non-empty) string back
        """
        module = self.module
        
        if sys.platform == "win32":
            # Check a variable that is already set
            env_var_name = 'USERNAME'  # this is always set (as is windir, ProgramFiles, USERPROFILE, etc.)
            expect_result = os.environ[env_var_name]
            self.assert_(expect_result, 'this should not be None or empty')
            # reason for using an existing OS variable is that unless the
            # MSVCRT dll imported is the exact same one that Python was
            # built with you can't share structures, see
            # http://msdn.microsoft.com/en-us/library/ms235460.aspx
            # "Potential Errors Passing CRT Objects Across DLL Boundaries"
        else:
            env_var_name = 'HELLO'
            os.environ[env_var_name] = 'WORLD'  # This doesn't work under win32
            expect_result = 'WORLD'
        
        result = module.getenv(env_var_name)
        self.failUnlessEqual(expect_result, result)

    def test_getenv_returns_null(self):
        """Related to issue 8. Test getenv of unset variable.
        """
        module = self.module
        env_var_name = 'NOT SET'
        expect_result = None
        try:
            # ensure variable is not set, ignoring not set errors
            del os.environ[env_var_name]
        except KeyError:
            pass
        result = module.getenv(env_var_name)
        self.failUnlessEqual(expect_result, result)


class StdBoolTest(unittest.TestCase):
    "Test correct parsing and generation of bool type"

    def setUp(self):
        """NOTE this is called once for each test* method
        (it is not called once per class).
        FIXME This is slightly inefficient as it is called *way* more times than it needs to be.
        """
        header_str = '''
#include <stdbool.h>

struct foo
{
    bool is_bar;
    int a;
};
'''
        self.module, _ = ctypesgentest.test(header_str)#, all_headers=True)

    def tearDown(self):
        del self.module
        ctypesgentest.cleanup()
        
    def test_stdbool_type(self):
        """Test is bool is correctly parsed"""
        module = self.module
        struct_foo = module.struct_foo
        self.failUnlessEqual(struct_foo._fields_, [("is_bar", ctypes.c_bool), ("a", ctypes.c_int)])


class SimpleMacrosTest(unittest.TestCase):
    """Based on simple_macros.py
    """
    
    def setUp(self):
        """NOTE this is called once for each test* method
        (it is not called once per class).
        FIXME This is slightly inefficient as it is called *way* more times than it needs to be.
        """
        header_str = '''
#define A 1
#define B(x,y) x+y
#define C(a,b,c) a?b:c
#define funny(x) "funny" #x
#define multipler_macro(x,y) x*y
#define minus_macro(x,y) x-y
#define divide_macro(x,y) x/y
#define mod_macro(x,y) x%y
'''
        libraries = None
        self.module, output = ctypesgentest.test(header_str)

    def tearDown(self):
        del self.module
        ctypesgentest.cleanup()

    def test_macro_constant_int(self):
        """Tests from simple_macros.py
        """
        module = self.module
        
        self.failUnlessEqual(module.A, 1)

    def test_macro_addition(self):
        """Tests from simple_macros.py
        """
        module = self.module
        
        self.failUnlessEqual(module.B(2, 2), 4)

    def test_macro_ternary_true(self):
        """Tests from simple_macros.py
        """
        module = self.module
        
        self.failUnlessEqual(module.C(True, 1, 2), 1)

    def test_macro_ternary_false(self):
        """Tests from simple_macros.py
        """
        module = self.module
        
        self.failUnlessEqual(module.C(False, 1, 2), 2)

    def test_macro_ternary_true_complex(self):
        """Test ?: with true, using values that can not be confused between True and 1
        """
        module = self.module
        
        self.failUnlessEqual(module.C(True, 99, 100), 99)

    def test_macro_ternary_false_complex(self):
        """Test ?: with false, using values that can not be confused between True and 1
        """
        module = self.module
        
        self.failUnlessEqual(module.C(False, 99, 100), 100)

    def test_macro_string_compose(self):
        """Tests from simple_macros.py
        """
        module = self.module
        
        self.failUnlessEqual(module.funny("bunny"), "funnybunny")
        
    def test_macro_math_multipler(self):
        module = self.module
        
        x, y = 2, 5
        self.failUnlessEqual(module.multipler_macro(x, y), x * y)

    def test_macro_math_minus(self):
        module = self.module
        
        x, y = 2, 5
        self.failUnlessEqual(module.minus_macro(x, y), x - y)

    def test_macro_math_divide(self):
        module = self.module
        
        x, y = 2, 5
        self.failUnlessEqual(module.divide_macro(x, y), x / y)

    def test_macro_math_mod(self):
        module = self.module
        
        x, y = 2, 5
        self.failUnlessEqual(module.mod_macro(x, y), x % y)


class StructuresTest(unittest.TestCase):
    """Based on structures.py
    """
    
    def setUp(self):
        """NOTE this is called once for each test* method
        (it is not called once per class).
        FIXME This is slightly inefficient as it is called *way* more times than it needs to be.
        """
        header_str = '''
struct foo
{
        int a;
        int b;
        int c;
};
'''
        libraries = None
        self.module, output = ctypesgentest.test(header_str)

    def tearDown(self):
        del self.module
        ctypesgentest.cleanup()

    def test_structures(self):
        """Tests from structures.py
        """
        module = self.module
        
        struct_foo = module.struct_foo
        self.failUnlessEqual(struct_foo._fields_, [("a", ctypes.c_int), ("b", ctypes.c_int), ("c", ctypes.c_int)])


class MathTest(unittest.TestCase):
    """Based on math_functions.py"""
    
    def setUp(self):
        """NOTE this is called once for each test* method
        (it is not called once per class).
        FIXME This is slightly inefficient as it is called *way* more times than it needs to be.
        """
        header_str = '#include <math.h>\n'
        if sys.platform == "win32":
            # pick something from %windir%\system32\msvc*dll that include stdlib
            libraries = ["msvcrt.dll"]
            libraries = ["msvcrt"]
        elif sys.platform.startswith("linux"):
            libraries = ["libm.so.6"]
        else:
            libraries = ["libc"]
        self.module, output = ctypesgentest.test(header_str, libraries=libraries, all_headers=True)

    def tearDown(self):
        del self.module
        ctypesgentest.cleanup()

    def test_sin(self):
        """Based on math_functions.py"""
        module = self.module
        
        self.failUnlessEqual(module.sin(2), math.sin(2))

    def test_sqrt(self):
        """Based on math_functions.py"""
        module = self.module
        
        self.failUnlessEqual(module.sqrt(4), 2)

        def local_test():
            module.sin("foobar")
        
        self.failUnlessRaises(ctypes.ArgumentError, local_test)

    def test_bad_args_string_not_number(self):
        """Based on math_functions.py"""
        module = self.module
        
        def local_test():
            module.sin("foobar")
        
        self.failUnlessRaises(ctypes.ArgumentError, local_test)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    ctypesgentest.ctypesgencore.messages.log.setLevel(logging.CRITICAL)  # do not log anything
    unittest.main()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
