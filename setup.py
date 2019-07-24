#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Examples:

        setup.py sdist bdist_wheel
        setup.py bdist_wininst
"""

from setuptools import setup

import six
import ctypesgencore

with open("README", "r") as fh:
    long_description = fh.read()
description = "Python wrapper generator for ctypes"
if six.PY2:
    long_description = description

setup(
    name="ctypesgen",
    maintainer="Alan Robertson",
    maintainer_email="alanr@unix.sh",
    version=ctypesgencore.VERSION,
    description=description,
    description_content_type="text/plain",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="https://github.com/Alan-R/ctypesgen",
    platforms=["any"],
    license="BSD 3-clause License",
    packages=[
        "ctypesgencore",
        "ctypesgencore.parser",
        "ctypesgencore.printer_python",
        "ctypesgencore.printer_json",
        "ctypesgencore.processor",
        "ctypesgencore.test",
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Software Development :: Build Tools",
    ],
    scripts=["ctypesgen.py"],
)
