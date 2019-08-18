import os
import sys
import io
import optparse
import glob

try:
    # should succeed for py3
    from importlib import reload as reload_module
except:
    reload_module = reload

sys.path.append(".")  # Allow tests to be called from parent directory with Python 2.6
sys.path.append("..")
import ctypesgen

"""ctypesgentest is a simple module for testing ctypesgen on various C constructs. It consists of a
single function, test(). test() takes a string that represents a C header file, along with some
keyword arguments representing options. It processes the header using ctypesgen and returns a tuple
containing the resulting module object and the output that ctypesgen produced."""

# set redirect_stdout to False if using console based debugger like pdb
redirect_stdout = True


def test(header, **more_options):

    assert isinstance(header, str)
    with open("temp.h", "w") as f:
      f.write(header)

    options = ctypesgen.options.get_default_options()
    options.headers = ["temp.h"]
    for opt in more_options:
        setattr(options, opt, more_options[opt])

    if redirect_stdout:
        # Redirect output
        sys.stdout = io.StringIO()

    # Step 1: Parse
    descriptions = ctypesgen.parser.parse(options.headers, options)

    # Step 2: Process
    ctypesgen.processor.process(descriptions, options)

    # Step 3: Print
    ctypesgen.printer.WrapperPrinter("temp.py", options, descriptions)

    if redirect_stdout:
        # Un-redirect output
        output = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = sys.__stdout__
    else:
        output = ''

    # Load the module we have just produced
    module = __import__("temp")
    reload_module(module)  # import twice, this hack ensure that "temp" is force loaded (there *must* be a better way to do this)

    return module, output


def cleanup(filepattern='temp.*'):
    fnames = glob.glob(filepattern)
    for fname in fnames:
        os.unlink(fname)
