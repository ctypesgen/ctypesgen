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

import unittest

import ctypesgentest  # TODO consider moving test() from ctypesgentest into this module


test_directory = os.path.abspath(os.path.dirname(__file__))

class StdlibTest(unittest.TestCase):
    
    def setUp(self):
        """NOTE this is called once for each test* method
        (it is not called once per class).
        FIXME This is slightly inefficient as it is called *way* more times than it needs to be.
        """
        header_str = '#include <stdlib.h>\n'
        if sys.platform == "win32":
            # pick something from %windir%\system32\msvc*dll that include stdlib
            libraries=["msvcrt.dll"]
            libraries=["msvcrt"]
        elif sys.platform == "linux2":
            libraries=["libc.so.6"]
        else:
            libraries=["libc"]
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
        else:
            env_var_name = 'HELLO'
            os.environ[env_var_name] = 'WORLD'  # This doesn't work under win32
            expect_result = 'WORLD'
        
        result = module.getenv(env_var_name)
        self.failUnlessEqual(expect_result, result)

    def test_getenv_returns_null(self):
        """Realted to issue 8. Test getenv of unset variable.
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


def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    unittest.main()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
