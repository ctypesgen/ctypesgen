#!/usr/bin/python

# The name wrap.py is obsolete - the main file for ctypesgen is now
# ctypesgen.py. This wrapper exists only to pass its arguments
# ctypesgen.py

import sys
execfile(sys.argv[0].replace("wrap.py","ctypesgen.py"))
