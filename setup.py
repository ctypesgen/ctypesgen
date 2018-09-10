#!/usr/bin/env python3
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Examples:

        setup.py sdist
        setup.py bdist_wininst

"""

from setuptools import setup, find_packages

import ctypesgencore

setup(name='ctypesgen',
    version=ctypesgencore.VERSION,
    description='Python wrapper generator for ctypes',
    url='http://code.google.com/p/ctypesgen/',
    license='BSD License',
    packages=find_packages(),
    scripts=['ctypesgen.py'])
