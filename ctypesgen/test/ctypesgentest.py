# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
import os
import sys
import io
import optparse
import glob
import json
from contextlib import contextmanager
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

if sys.version_info.major == 2:
    import imp
else:
    import types

# ensure that we can load the ctypesgen library
PACKAGE_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
sys.path.insert(0, PACKAGE_DIR)
import ctypesgen


"""ctypesgentest is a simple module for testing ctypesgen on various C constructs. It consists of a
single function, test(). test() takes a string that represents a C header file, along with some
keyword arguments representing options. It processes the header using ctypesgen and returns a tuple
containing the resulting module object and the output that ctypesgen produced."""

# set redirect_stdout to False if using console based debugger like pdb
redirect_stdout = True

@contextmanager
def redirect(stdout=sys.stdout):
    backup = sys.stdout
    sys.stdout = stdout
    try:
        yield stdout
    finally:
        sys.stdout = backup

def test(header, **more_options):

    assert isinstance(header, str)
    with open("temp.h", "w") as f:
        f.write(header)

    options = ctypesgen.options.get_default_options()
    options.headers = ["temp.h"]
    for opt, val in more_options.items():
        setattr(options, opt, val)

    if redirect_stdout:
        # Redirect output
        sys.stdout = io.StringIO()

    # Step 1: Parse
    descriptions = ctypesgen.parser.parse(options.headers, options)

    # Step 2: Process
    ctypesgen.processor.process(descriptions, options)

    # Step 3: Print
    printer = None
    if options.output_language.startswith("py"):
        def module_from_code(name, python_code):
            module = imp.new_module(name) \
                    if sys.version_info.major == 2 \
                    else types.ModuleType(name) 
            exec(python_code, module.__dict__)
            return module
        
        # we have to redirect stdout, as WrapperPrinter is only able to write to files or stdout
        with redirect(stdout=StringIO()) as printer_output:
            # do not discard WrapperPrinter object, as the target file gets closed on printer deletion
            _ = ctypesgen.printer_python.WrapperPrinter(None, options, descriptions)
            generated_python_code = printer_output.getvalue()
            module = module_from_code('temp', generated_python_code)
            retval = module

    elif options.output_language == "json":
        # for ease and consistency with test results, we are going to cheat by
        # resetting the anonymous tag number
        ctypesgen.ctypedescs.last_tagnum = 0
        ctypesgen.printer_json.WrapperPrinter("temp.json", options, descriptions)
        with open("temp.json") as f:
            JSON = json.load(f)
        retval = JSON
    else:
        raise RuntimeError("No such output language `" + options.output_language + "'")

    if redirect_stdout:
        # Un-redirect output
        output = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = sys.__stdout__
    else:
        output = ""

    return retval, output


def cleanup(filepattern="temp.*"):
    fnames = glob.glob(filepattern)
    for fname in fnames:
        os.unlink(fname)
