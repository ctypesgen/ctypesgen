#!/usr/bin/env python3
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Examples:

        setup.py sdist
        setup.py bdist_wininst

"""

import os
from setuptools import setup, find_packages

THIS_DIR = os.path.dirname(__file__)

import ctypesgen

ctypesgen.version.write_version_file()

VERSION_FILE = os.path.relpath(ctypesgen.version.VERSION_FILE, THIS_DIR)
f = open("MANIFEST.in", "w")
f.write("include {}\n".format(VERSION_FILE))
f.write("graft ctypesgen\n")
f.write("recursive-exclude ctypesgen .gitignore\n")
f.close()

try:
    setup(
        name="ctypesgen",
        version=ctypesgen.VERSION.partition("-g")[0],
        description="Python wrapper generator for ctypes",
        long_description="ctypesgen reads parses c header files and creates a wrapper for "
        "libraries based on what it finds.  Preprocessor macros are handled "
        "in a manner consistent with typical c code.  Preprocessor macro "
        "functions are translated into Python functions that are then made "
        "available to the user of the newly-generated Python wrapper "
        "library.\n"
        "ctypesgen can also output JSON, which can be used with Mork, "
        "which generates bindings for Lua, using the alien module (which "
        "binds libffi to Lua).",
        long_description_content_type="text/plain",
        url="https://github.com/davidjamesca/ctypesgen",
        license="BSD License",
        packages=find_packages(),
        include_package_data=True,
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
        entry_points={"console_scripts": ["ctypesgen = ctypesgen.main:main"]},
    )
finally:
    os.unlink("MANIFEST.in")
