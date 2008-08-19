#!/usr/bin/env python

from distutils.core import setup

setup(name='ctypesgen',
    version='0.0',
    description='Python wrapper generator for ctypes',
    url='http://code.google.com/p/ctypesgen/',
    license='BSD License',
    packages=['ctypesgencore',
        'ctypesgencore.parser',
        'ctypesgencore.printer',
        'ctypesgencore.processor'],
    scripts=['ctypesgen.py'])
