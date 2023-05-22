#!/usr/bin/env python3

import sys
import os

# ensure that we can load the ctypesgen library
THIS_DIR = os.path.dirname(__file__)
sys.path.insert(0, THIS_DIR)

from ctypesgen.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
