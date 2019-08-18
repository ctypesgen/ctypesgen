#!/usr/bin/env python3
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Examples:

        setup.py sdist
        setup.py bdist_wininst

"""

import os
from setuptools import setup, find_packages

THIS_DIR = os.path.dirname( __file__ )

import ctypesgen

ctypesgen.version.write_version_file()

VERSION_FILE = os.path.relpath(ctypesgen.version.VERSION_FILE, THIS_DIR)
f = open('MANIFEST.in', 'w')
f.write('include {}\n'.format(VERSION_FILE))
f.write('graft ctypesgen\n')
f.close()

try:
    setup(
        name='ctypesgen',
        version=ctypesgen.VERSION.partition('-g')[0],
        description='Python wrapper generator for ctypes',
        long_description=
            'ctypesgen reads parses c header files and creates a wrapper for '
            'libraries base on what it finds.  Preprocessor macros are handled '
            'in a manner consistent with typical c code.  Preprocessor macro '
            'functions are translated into Python functions that are then made '
            'available to the user of the newly-generated Python wrapper '
            'library.\n'
            'ctypesgen can also output JSON, which can be used with Mork, '
            'which generates bindings for Lua, using the alien module (which '
            'binds libffi to Lua).',
        url='https://github.com/olsonse/ctypesgen',
        license='BSD License',
        packages=find_packages(),
        include_package_data=True,
        entry_points={
          'console_scripts': [
            'ctypesgen = ctypesgen.main:main',
          ],
        },
    )
finally:
    os.unlink('MANIFEST.in')
