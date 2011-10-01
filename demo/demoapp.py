#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""
Trivial ctypesgen demo library consumer
from http://code.google.com/p/ctypesgen

 NOTE demolib.py needs to be generated via:

    ../ctypesgen.py -o pydemolib.py -l demolib demolib.h
    ../ctypesgen.py -o pydemolib.py -l demolib.so demolib.h


"""

import sys

import pydemolib  # generated from demolib.h by ctypesgen


def do_demo():
    a = 1
    b = 2
    result = pydemolib.trivial_add(a, b)
    print "a", a
    print "b", b
    print "result", result


def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    do_demo()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
