#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Examples:

        setup.py sdist
        setup.py bdist_wininst

"""

from distutils.core import setup

import ctypesgencore

setup(
    name="ctypesgen",
    maintainer="Alan Robertson",
    maintainer_email="alanr@unix.sh",
    version=ctypesgencore.VERSION,
    description="Python wrapper generator for ctypes",
    url="https://github.com/Alan-R/ctypesgen",
    license="BSD License",
    packages=[
        "ctypesgencore",
        "ctypesgencore.parser",
        "ctypesgencore.printer_python",
        "ctypesgencore.printer_json",
        "ctypesgencore.processor",
        "ctypesgencore.test",
    ],
    scripts=["ctypesgen.py"],
)
