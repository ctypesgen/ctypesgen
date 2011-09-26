#!/usr/bin/env python
# -*- coding: us-ascii -*-
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
        'ctypesgencore.printer_python',
        'ctypesgencore.printer_json',
        'ctypesgencore.processor'],
    scripts=['ctypesgen.py'])
