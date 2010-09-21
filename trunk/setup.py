#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Examples:

        setup.py sdist
        setup.py bdist_wininst

"""

from distutils.core import setup

import ctypesgencore

setup(name='ctypesgen',
    version=ctypesgencore.VERSION,
    description='Python wrapper generator for ctypes',
    url='http://code.google.com/p/ctypesgen/',
    license='BSD License',
    packages=['ctypesgencore',
        'ctypesgencore.parser',
        'ctypesgencore.printer',
        'ctypesgencore.processor'],
    scripts=['ctypesgen.py'])
