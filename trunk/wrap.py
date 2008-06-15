#!/usr/bin/env python

'''Generate a Python ctypes wrapper file for a header file.

Usage example::
    wrap.py -lGL -oGL.py /usr/include/GL/gl.h

    >>> from GL import *

'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: wrap.py 738 2007-03-12 04:53:42Z Alex.Holkner $'

from ctypesparser import *
import textwrap
import optparse, os, re, sys, tempfile
from errno import ENOENT
from ctypes import CDLL, RTLD_GLOBAL, c_byte
from ctypes.util import find_library
from glob import glob
import ctypestemplate
from ctypestemplate import load_library

class CtypesWrapper(CtypesParser, CtypesTypeVisitor):
    file=None
    def begin_output(self, output_file, library, link_modules=(), 
                     emit_filenames=(), all_headers=False,
                     include_symbols=None, exclude_symbols=None,
                     save_preprocessed_headers=None,
                     libdirs=None):
        self.library = library
        self.file = output_file
        self.all_names = []
        self.known_types = {}
        self.structs = set()
        self.opaque_structs = set()
        self.enums = set()
        self.emit_filenames = emit_filenames
        self.all_headers = all_headers
        self.include_symbols = None
        self.exclude_symbols = None
        if include_symbols:
            self.include_symbols = re.compile(include_symbols)
        if exclude_symbols:
            self.exclude_symbols = re.compile(exclude_symbols)
        self.preprocessor_parser.save_preprocessed_headers = \
            save_preprocessed_headers
        self.libdirs = libdirs

        self.linked_symbols = {}
        for name in link_modules:
            module = __import__(name, globals(), locals(), ['foo'])
            for symbol in dir(module):
                if symbol not in self.linked_symbols:
                    self.linked_symbols[symbol] = '%s.%s' % (name, symbol)
        self.link_modules = link_modules

        self.print_preamble()
        self.print_link_modules_imports()

    def wrap(self, filename, source=None):
        assert self.file, 'Call begin_output first'
        self.parse(filename, source)

    def end_output(self):
        self.print_epilogue()
        self.file = None

    def does_emit(self, symbol, filename, restype=None, argtypes=[]):

        # Skip any functions which mention excluded types
        if self.exclude_symbols:
            for a in [symbol, restype] + argtypes:
                if a and self.exclude_symbols.match(str(a)):
                    return

        if self.include_symbols and not re.match(self.include_symbols, symbol):
            return False

        return self.all_headers or filename in self.emit_filenames

    def print_preamble(self):
        import textwrap
        import time
        path = os.environ.get('LD_LIBRARY_PATH',None)
        if path:
            self.libdirs += [path]
        print >> self.file, textwrap.dedent("""
            '''Wrapper for %(library)s
            
            Generated with:
            %(argv)s
            
            Do not modify this file.
            '''

            __docformat__ =  'restructuredtext'

            import ctypes, os
            from ctypes import *
            from UserString import UserString, MutableString

            _int_types = (c_int16, c_int32)
            if hasattr(ctypes, 'c_int64'):
                # Some builds of ctypes apparently do not have c_int64
                # defined; it's a pretty good bet that these builds do not
                # have 64-bit pointers.
                _int_types += (ctypes.c_int64,)
            for t in _int_types:
                if sizeof(t) == sizeof(c_size_t):
                    c_ptrdiff_t = t

            class c_void(Structure):
                # c_void_p is a buggy return type, converting to int, so
                # POINTER(None) == c_void_p is actually written as
                # POINTER(c_void), so it can be treated as a real pointer.
                _fields_ = [('dummy', c_int)]

            class String(MutableString, Union):

                _fields_ = [('raw', POINTER(c_char)),
                            ('data', c_char_p)]

                def __init__(self, obj=""):

                    if isinstance(obj, (str, unicode, UserString)):
                        self.data = str(obj)
                    else:
                        self.raw = obj

                def from_param(cls, obj):

                    # Convert None or 0
                    if obj is None or obj == 0:
                        return None

                    # Convert from String
                    elif isinstance(obj, String):
                        return obj

                    # Convert from str
                    elif isinstance(obj, str):
                        return cls(obj)

                    # Convert from raw pointer
                    elif isinstance(obj, int):
                        return cls(cast(obj, POINTER(c_char)))

                    # Convert from object
                    else:
                        return String.from_param(obj._as_parameter_)
                from_param = classmethod(from_param)

            def ReturnString(obj):
                return String.from_param(obj)

            _libs = {}

            # As of ctypes 1.0, ctypes does not support custom error-checking
            # functions on callbacks, nor does it support custom datatypes on
            # callbacks, so we must ensure that all callbacks return
            # primitive datatypes.
            #
            # Non-primitive return values wrapped with UNCHECKED won't be
            # typechecked, and will be converted to c_void_p.
            def UNCHECKED(type):
                if (hasattr(type, "_type_") and isinstance(type._type_, str)
                    and type._type_ != "P"):
                    return type
                else:
                    return c_void_p

            path = os.environ.get('LD_LIBRARY_PATH',None)
            if path:
                os.environ['LD_LIBRARY_PATH'] = %(libdirs)r + ':' + path
            else:
                os.environ['LD_LIBRARY_PATH'] = %(libdirs)r
        """ % {
            'library': str(self.library),
            'date': time.ctime(),
            'class': self.__class__.__name__,
            'argv': ' '.join(sys.argv),
            'libdirs': ':'.join(self.libdirs) 
        }).lstrip()
        template_file = os.path.join(os.path.dirname(ctypestemplate.__file__), "ctypestemplate.py")
        print >> self.file, open(template_file, "r").read()
        os.environ['LD_LIBRARY_PATH'] = ':'.join(self.libdirs)
        self.loaded_libraries = []
        self.short_library_name = {}
        for library in self.library:
            lib = load_library(library)
            if lib:
                self.short_library_name[lib._name] = library
                self.loaded_libraries.append(lib)
                print >>self.file, textwrap.dedent("""
                    _libs[%r] = load_library(%r)
                """ % (library, library))

    def print_link_modules_imports(self):
        for name in self.link_modules:
            print >> self.file, 'from %s import *' % name
        print >> self.file

    def print_epilogue(self):

        # Print out defines        
        self.preprocessor_parser.emit(self.file, self.include_symbols,
                                      self.all_names, self.all_headers,
                                      self.emit_filenames,
                                      self.linked_symbols)


    def handle_ctypes_constant(self, name, value, filename, lineno):
        if self.does_emit(name, filename):
            if name not in self.linked_symbols:
                print >> self.file, '%s = %r' % (name, value),
                print >> self.file, '\t# %s:%d' % (filename, lineno)
            self.all_names.append(name)

    def handle_ctypes_type_definition(self, name, ctype, filename, lineno):
        if self.does_emit(name, filename):
            if name not in self.linked_symbols:
                ctype.visit(self)
                self.emit_type(ctype)
                if name not in self.all_names:
                    print >> self.file, '%s = %s' % (name, str(ctype)),
                    print >> self.file, '\t# %s:%d' % (filename, lineno)
            self.all_names.append(name)
        else:
            self.known_types[name] = (ctype, filename, lineno)

    def emit_type(self, t):
        t.visit(self)
        for s in t.get_required_type_names():
            if s in self.known_types:
                if s not in self.linked_symbols:
                    s_ctype, s_filename, s_lineno = self.known_types[s]
                    s_ctype.visit(self)

                    self.emit_type(s_ctype)
                    print >> self.file, '%s = %s' % (s, str(s_ctype)),
                    print >> self.file, '\t# %s:%d' % (s_filename, s_lineno)
                del self.known_types[s]

    def visit_struct(self, struct):
        if struct.tag in self.linked_symbols:
            return
        
        # Output struct definition
        if struct.tag not in self.opaque_structs:
            base = {True: 'Union', False: 'Structure'}[struct.is_union]
            print >> self.file, 'class struct_%s(%s):' % (struct.tag, base)
            print >> self.file, '    pass'
            self.opaque_structs.add(struct.tag)

        # Set fields after completing class, so incomplete structs can be
        # referenced within struct.
        for name, typ in struct.members:
            self.emit_type(typ)

        if struct.tag not in self.structs and not struct.opaque:
            self.structs.add(struct.tag)
            print >> self.file, 'struct_%s.__slots__ = [' % struct.tag
            for m in struct.members:
                print >> self.file, "    '%s'," % m[0]
            print >> self.file, ']'
            print >> self.file, 'struct_%s._fields_ = [' % struct.tag
            for m in struct.members:
                print >> self.file, "    ('%s', %s)," % (m[0], m[1])
            print >> self.file, ']'
            print >> self.file

    def visit_enum(self, enum):
        if enum.tag in self.linked_symbols:
            return
        if enum.tag in self.enums:
            return
        self.enums.add(enum.tag)

        print >> self.file, 'enum_%s = c_int' % enum.tag
        for name, value in enum.enumerators:
            self.all_names.append(name)
            print >> self.file, '%s = %d' % (name, value)

    def handle_ctypes_function(self, name, restype, argtypes, filename, lineno):
        if name in self.linked_symbols:
            return

        if self.does_emit(name, filename, restype, argtypes):

            # Also emit any types this func requires that haven't yet been
            # written.
            self.emit_type(restype)
            for a in argtypes:
                self.emit_type(a)

            for lib in self.loaded_libraries:
                if hasattr(lib, name):
                    self.all_names.append(name)
                    library = self.short_library_name[lib._name]
                    print >> self.file, '# %s:%d' % (filename, lineno)
                    print >> self.file, 'if hasattr(_libs[%r], %r):' % (library, name)
                    print >> self.file, '  %s = _libs[%r].%s' % (name, library, name)
                    print >> self.file, '  %s.restype = %s' % (name, str(restype))
                    print >> self.file, '  %s.argtypes = [%s]' % \
                        (name, ', '.join([str(a) for a in argtypes])) 
                    print >> self.file
                    break

    def handle_ctypes_variable(self, name, ctype, filename, lineno):
        if name in self.linked_symbols:
            return

        if self.does_emit(name, filename):
            self.emit_type(ctype)
            for lib in self.loaded_libraries:
                try:
                    c_byte.in_dll(lib, name)
                except:
                    pass
                else:
                    print >> self.file, 'try:'
                    print >> self.file, '  %s = (%s).in_dll(_libs[%r], %r)' % \
                        (name, str(ctype), self.short_library_name[lib._name], name)
                    print >> self.file, 'except:'
                    print >> self.file, '  pass'
                    self.all_names.append(name)
                    break

def option_W(option, opt, value, parser):
    if len(value) < 4 or value[0:3] != 'l,-':
        raise optparse.BadOptionError("not in '-Wl,<opt>' form: %s%s"
                                      % (opt, value))
    opt = value[2:]
    if opt not in ['-L', '-R', '--rpath']:
        raise optparse.BadOptionError("-Wl option must be -L, -R"
                                      " or --rpath, not " + value[2:])
    # Push the linker option onto the list for further parsing.
    parser.rargs.insert(0, value)

def main(*argv):
    from tempfile import NamedTemporaryFile

    usage = 'usage: %prog [options] <header.h>'
    op = optparse.OptionParser(usage=usage)
    op.add_option('-o', '--output', dest='output',
                  help='write wrapper to FILE', metavar='FILE')
    op.add_option('-l', '--library', dest='library', action='append',
                  help='link to LIBRARY', metavar='LIBRARY', default=[])
    op.add_option('-m', '--link-module', action='append', dest='link_modules',
                  help='use symbols from MODULE', metavar='MODULE',
                  default=[])
    op.add_option('-a', '--all-headers', action='store_true',
                  dest='all_headers',
                  help='include symbols from all headers', default=False)
    op.add_option('-i', '--include-symbols', dest='include_symbols',
                  help='regular expression for symbols to include')
    op.add_option('-x', '--exclude-symbols', dest='exclude_symbols',
                  help='regular expression for symbols to exclude')
    op.add_option('', '--cpp', dest='cpp',
                  help='The command to invoke the c preprocessor, including any necessary options (default: gcc -E)')
    op.add_option('', '--save-preprocessed-headers', dest='filename',
                  help='Save the preprocessed headers to the specified '
                       'FILENAME')
    op.add_option("-W", action="callback", callback=option_W, type='str',
                  metavar="l,OPTION",
                  help="where OPTION is -L, -R, or --rpath")
    op.add_option("-L", "-R", "--rpath", action="append", dest="libdirs",
                  metavar="LIBDIR", help="Add LIBDIR to the search path")

    (options, args) = op.parse_args(list(argv[1:]))
    if len(args) < 1:
        print >> sys.stderr, 'No header files specified.'
        sys.exit(1)
    headers = args

    if options.output is None:
        print >> sys.stderr, 'No output file specified.'
        sys.exit(1)

    if len(options.library) == 0:
        print >> sys.stderr, 'No libraries specified.'

    wrapper = CtypesWrapper()
    wrapper.begin_output(open(options.output, 'w'), 
                         library=options.library, 
                         emit_filenames=headers,
                         link_modules=options.link_modules,
                         all_headers=options.all_headers,
                         include_symbols=options.include_symbols,
                         exclude_symbols=options.exclude_symbols,
                         save_preprocessed_headers=options.filename,
                         libdirs=options.libdirs,
                         )
    wrapper.preprocessor_parser.cpp = options.cpp

    f = NamedTemporaryFile(suffix=".h")
    for header in headers:
        print >>f, '#include "%s"' % header
    f.flush()
    wrapper.wrap(f.name)
    wrapper.end_output()

    print 'Wrapped to %s' % options.output

if __name__ == '__main__':
    main(*sys.argv)