import optparse, sys
sys.path.append("..")
import ctypesgencore

"""ctypesgentest is a simple module for testing ctypesgen on various C constructs. It consists of a
single function, test(). test() takes a string that represents a C header file. It processes the
header using ctypesgen and returns the resulting module object."""

def test(header):

	assert isinstance(header, str)
	file("temp.h","w").write(header)
	
	options = ctypesgencore.options.get_default_options()
	options.headers = ["temp.h"]
	
	# Step 1: Parse
	descriptions=ctypesgencore.parser.parse(options.headers,options)
	
	# Step 2: Process
	ctypesgencore.processor.process(descriptions,options)
	
	# Step 3: Print
	ctypesgencore.printer.WrapperPrinter("temp.py",options,descriptions)
	
	# Load the module we have just produced
	module = __import__("temp")
	return module