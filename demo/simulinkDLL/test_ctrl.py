r"""Wrapper for test_ctrl.h

Generated with:
C:\Prj\GitHub\ctypesgen\venv\Scripts\ctypesgen -lC:\Prj\GitHub\ctypesgen\demo\simulinkDLL\test_ctrl_win64.dll C:\Prj\GitHub\ctypesgen\demo\simulinkDLL\test_ctrl.h --include rtwtypes.h --allow-gnu-c -IC:\Prj\GitHub\ctypesgen\demo\simulinkDLL -oC:\Prj\GitHub\ctypesgen\demo\simulinkDLL\test_ctrl.py

Do not modify this file.
"""

__docformat__ = "restructuredtext"

# Begin preamble for Python

import ctypes
import sys
from ctypes import *  # noqa: F401, F403

_int_types = (ctypes.c_int16, ctypes.c_int32)
if hasattr(ctypes, "c_int64"):
    # Some builds of ctypes apparently do not have ctypes.c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (ctypes.c_int64,)
for t in _int_types:
    if ctypes.sizeof(t) == ctypes.sizeof(ctypes.c_size_t):
        c_ptrdiff_t = t
del t
del _int_types



class UserString:
    def __init__(self, seq):
        if isinstance(seq, bytes):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq).encode()

    def __bytes__(self):
        return self.data

    def __str__(self):
        return self.data.decode()

    def __repr__(self):
        return repr(self.data)

    def __int__(self):
        return int(self.data.decode())

    def __long__(self):
        return int(self.data.decode())

    def __float__(self):
        return float(self.data.decode())

    def __complex__(self):
        return complex(self.data.decode())

    def __hash__(self):
        return hash(self.data)

    def __le__(self, string):
        if isinstance(string, UserString):
            return self.data <= string.data
        else:
            return self.data <= string

    def __lt__(self, string):
        if isinstance(string, UserString):
            return self.data < string.data
        else:
            return self.data < string

    def __ge__(self, string):
        if isinstance(string, UserString):
            return self.data >= string.data
        else:
            return self.data >= string

    def __gt__(self, string):
        if isinstance(string, UserString):
            return self.data > string.data
        else:
            return self.data > string

    def __eq__(self, string):
        if isinstance(string, UserString):
            return self.data == string.data
        else:
            return self.data == string

    def __ne__(self, string):
        if isinstance(string, UserString):
            return self.data != string.data
        else:
            return self.data != string

    def __contains__(self, char):
        return char in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.__class__(self.data[index])

    def __getslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, bytes):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other).encode())

    def __radd__(self, other):
        if isinstance(other, bytes):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other).encode() + self.data)

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self):
        return self.__class__(self.data.capitalize())

    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))

    def count(self, sub, start=0, end=sys.maxsize):
        return self.data.count(sub, start, end)

    def decode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())

    def encode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())

    def endswith(self, suffix, start=0, end=sys.maxsize):
        return self.data.endswith(suffix, start, end)

    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))

    def find(self, sub, start=0, end=sys.maxsize):
        return self.data.find(sub, start, end)

    def index(self, sub, start=0, end=sys.maxsize):
        return self.data.index(sub, start, end)

    def isalpha(self):
        return self.data.isalpha()

    def isalnum(self):
        return self.data.isalnum()

    def isdecimal(self):
        return self.data.isdecimal()

    def isdigit(self):
        return self.data.isdigit()

    def islower(self):
        return self.data.islower()

    def isnumeric(self):
        return self.data.isnumeric()

    def isspace(self):
        return self.data.isspace()

    def istitle(self):
        return self.data.istitle()

    def isupper(self):
        return self.data.isupper()

    def join(self, seq):
        return self.data.join(seq)

    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))

    def lower(self):
        return self.__class__(self.data.lower())

    def lstrip(self, chars=None):
        return self.__class__(self.data.lstrip(chars))

    def partition(self, sep):
        return self.data.partition(sep)

    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))

    def rfind(self, sub, start=0, end=sys.maxsize):
        return self.data.rfind(sub, start, end)

    def rindex(self, sub, start=0, end=sys.maxsize):
        return self.data.rindex(sub, start, end)

    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))

    def rpartition(self, sep):
        return self.data.rpartition(sep)

    def rstrip(self, chars=None):
        return self.__class__(self.data.rstrip(chars))

    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)

    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)

    def splitlines(self, keepends=0):
        return self.data.splitlines(keepends)

    def startswith(self, prefix, start=0, end=sys.maxsize):
        return self.data.startswith(prefix, start, end)

    def strip(self, chars=None):
        return self.__class__(self.data.strip(chars))

    def swapcase(self):
        return self.__class__(self.data.swapcase())

    def title(self):
        return self.__class__(self.data.title())

    def translate(self, *args):
        return self.__class__(self.data.translate(*args))

    def upper(self):
        return self.__class__(self.data.upper())

    def zfill(self, width):
        return self.__class__(self.data.zfill(width))


class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""

    def __init__(self, string=""):
        self.data = string

    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")

    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + sub + self.data[index + 1 :]

    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + self.data[index + 1 :]

    def __setslice__(self, start, end, sub):
        start = max(start, 0)
        end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start] + sub.data + self.data[end:]
        elif isinstance(sub, bytes):
            self.data = self.data[:start] + sub + self.data[end:]
        else:
            self.data = self.data[:start] + str(sub).encode() + self.data[end:]

    def __delslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]

    def immutable(self):
        return UserString(self.data)

    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, bytes):
            self.data += other
        else:
            self.data += str(other).encode()
        return self

    def __imul__(self, n):
        self.data *= n
        return self


class String(MutableString, ctypes.Union):
    _fields_ = [("raw", ctypes.POINTER(ctypes.c_char)), ("data", ctypes.c_char_p)]

    def __init__(self, obj=b""):
        if isinstance(obj, (bytes, UserString)):
            self.data = bytes(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(ctypes.POINTER(ctypes.c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from bytes
        elif isinstance(obj, bytes):
            return cls(obj)

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj.encode())

        # Convert from c_char_p
        elif isinstance(obj, ctypes.c_char_p):
            return obj

        # Convert from POINTER(ctypes.c_char)
        elif isinstance(obj, ctypes.POINTER(ctypes.c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(ctypes.cast(obj, ctypes.POINTER(ctypes.c_char)))

        # Convert from ctypes.c_char array
        elif isinstance(obj, ctypes.c_char * len(obj)):
            return obj

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)

    from_param = classmethod(from_param)


def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)


# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to ctypes.c_void_p.
def UNCHECKED(type):
    if hasattr(type, "_type_") and isinstance(type._type_, str) and type._type_ != "P":
        return type
    else:
        return ctypes.c_void_p


# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self, func, restype, argtypes, errcheck):
        self.func = func
        self.func.restype = restype
        self.argtypes = argtypes
        if errcheck:
            self.func.errcheck = errcheck

    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func

    def __call__(self, *args):
        fixed_args = []
        i = 0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i += 1
        return self.func(*fixed_args + list(args[i:]))


def ord_if_char(value):
    """
    Simple helper used for casts to simple builtin types:  if the argument is a
    string type, it will be converted to it's ordinal value.

    This function will raise an exception if the argument is string with more
    than one characters.
    """
    return ord(value) if (isinstance(value, bytes) or isinstance(value, str)) else value

# End preamble

_libs = {}
_libdirs = []

# Begin loader

"""
Load libraries - appropriately for all our supported platforms
"""
# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import ctypes
import ctypes.util
import glob
import os.path
import platform
import re
import sys


def _environ_path(name):
    """Split an environment variable into a path-like list elements"""
    if name in os.environ:
        return os.environ[name].split(":")
    return []


class LibraryLoader:
    """
    A base class For loading of libraries ;-)
    Subclasses load libraries for specific platforms.
    """

    # library names formatted specifically for platforms
    name_formats = ["%s"]

    class Lookup:
        """Looking up calling conventions for a platform"""

        mode = ctypes.DEFAULT_MODE

        def __init__(self, path):
            super(LibraryLoader.Lookup, self).__init__()
            self.access = dict(cdecl=ctypes.CDLL(path, self.mode))

        def get(self, name, calling_convention="cdecl"):
            """Return the given name according to the selected calling convention"""
            if calling_convention not in self.access:
                raise LookupError(
                    "Unknown calling convention '{}' for function '{}'".format(
                        calling_convention, name
                    )
                )
            return getattr(self.access[calling_convention], name)

        def has(self, name, calling_convention="cdecl"):
            """Return True if this given calling convention finds the given 'name'"""
            if calling_convention not in self.access:
                return False
            return hasattr(self.access[calling_convention], name)

        def __getattr__(self, name):
            return getattr(self.access["cdecl"], name)

    def __init__(self):
        self.other_dirs = []

    def __call__(self, libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            # noinspection PyBroadException
            try:
                return self.Lookup(path)
            except Exception:  # pylint: disable=broad-except
                pass

        raise ImportError("Could not load %s." % libname)

    def getpaths(self, libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # search through a prioritized series of locations for the library

            # we first search any specific directories identified by user
            for dir_i in self.other_dirs:
                for fmt in self.name_formats:
                    # dir_i should be absolute already
                    yield os.path.join(dir_i, fmt % libname)

            # check if this code is even stored in a physical file
            try:
                this_file = __file__
            except NameError:
                this_file = None

            # then we search the directory where the generated python interface is stored
            if this_file is not None:
                for fmt in self.name_formats:
                    yield os.path.abspath(os.path.join(os.path.dirname(__file__), fmt % libname))

            # now, use the ctypes tools to try to find the library
            for fmt in self.name_formats:
                path = ctypes.util.find_library(fmt % libname)
                if path:
                    yield path

            # then we search all paths identified as platform-specific lib paths
            for path in self.getplatformpaths(libname):
                yield path

            # Finally, we'll try the users current working directory
            for fmt in self.name_formats:
                yield os.path.abspath(os.path.join(os.path.curdir, fmt % libname))

    def getplatformpaths(self, _libname):  # pylint: disable=no-self-use
        """Return all the library paths available in this platform"""
        return []


# Darwin (Mac OS X)


class DarwinLibraryLoader(LibraryLoader):
    """Library loader for MacOS"""

    name_formats = [
        "lib%s.dylib",
        "lib%s.so",
        "lib%s.bundle",
        "%s.dylib",
        "%s.so",
        "%s.bundle",
        "%s",
    ]

    class Lookup(LibraryLoader.Lookup):
        """
        Looking up library files for this platform (Darwin aka MacOS)
        """

        # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
        # of the default RTLD_LOCAL.  Without this, you end up with
        # libraries not being loadable, resulting in "Symbol not found"
        # errors
        mode = ctypes.RTLD_GLOBAL

    def getplatformpaths(self, libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [fmt % libname for fmt in self.name_formats]

        for directory in self.getdirs(libname):
            for name in names:
                yield os.path.join(directory, name)

    @staticmethod
    def getdirs(libname):
        """Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        """

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [
                os.path.expanduser("~/lib"),
                "/usr/local/lib",
                "/usr/lib",
            ]

        dirs = []

        if "/" in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
            dirs.extend(_environ_path("LD_RUN_PATH"))

        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "macosx_app":
            dirs.append(os.path.join(os.environ["RESOURCEPATH"], "..", "Frameworks"))

        dirs.extend(dyld_fallback_library_path)

        return dirs


# Posix


class PosixLibraryLoader(LibraryLoader):
    """Library loader for POSIX-like systems (including Linux)"""

    _ld_so_cache = None

    _include = re.compile(r"^\s*include\s+(?P<pattern>.*)")

    name_formats = ["lib%s.so", "%s.so", "%s"]

    class _Directories(dict):
        """Deal with directories"""

        def __init__(self):
            dict.__init__(self)
            self.order = 0

        def add(self, directory):
            """Add a directory to our current set of directories"""
            if len(directory) > 1:
                directory = directory.rstrip(os.path.sep)
            # only adds and updates order if exists and not already in set
            if not os.path.exists(directory):
                return
            order = self.setdefault(directory, self.order)
            if order == self.order:
                self.order += 1

        def extend(self, directories):
            """Add a list of directories to our set"""
            for a_dir in directories:
                self.add(a_dir)

        def ordered(self):
            """Sort the list of directories"""
            return (i[0] for i in sorted(self.items(), key=lambda d: d[1]))

    def _get_ld_so_conf_dirs(self, conf, dirs):
        """
        Recursive function to help parse all ld.so.conf files, including proper
        handling of the `include` directive.
        """

        try:
            with open(conf) as fileobj:
                for dirname in fileobj:
                    dirname = dirname.strip()
                    if not dirname:
                        continue

                    match = self._include.match(dirname)
                    if not match:
                        dirs.add(dirname)
                    else:
                        for dir2 in glob.glob(match.group("pattern")):
                            self._get_ld_so_conf_dirs(dir2, dirs)
        except IOError:
            pass

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = self._Directories()
        for name in (
            "LD_LIBRARY_PATH",
            "SHLIB_PATH",  # HP-UX
            "LIBPATH",  # OS/2, AIX
            "LIBRARY_PATH",  # BE/OS
        ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))

        self._get_ld_so_conf_dirs("/etc/ld.so.conf", directories)

        bitage = platform.architecture()[0]

        unix_lib_dirs_list = []
        if bitage.startswith("64"):
            # prefer 64 bit if that is our arch
            unix_lib_dirs_list += ["/lib64", "/usr/lib64"]

        # must include standard libs, since those paths are also used by 64 bit
        # installs
        unix_lib_dirs_list += ["/lib", "/usr/lib"]
        if sys.platform.startswith("linux"):
            # Try and support multiarch work in Ubuntu
            # https://wiki.ubuntu.com/MultiarchSpec
            if bitage.startswith("32"):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ["/lib/i386-linux-gnu", "/usr/lib/i386-linux-gnu"]
            elif bitage.startswith("64"):
                # Assume Intel/AMD x86 compatible
                unix_lib_dirs_list += [
                    "/lib/x86_64-linux-gnu",
                    "/usr/lib/x86_64-linux-gnu",
                ]
            else:
                # guess...
                unix_lib_dirs_list += glob.glob("/lib/*linux-gnu")
        directories.extend(unix_lib_dirs_list)

        cache = {}
        lib_re = re.compile(r"lib(.*)\.s[ol]")
        # ext_re = re.compile(r"\.s[ol]$")
        for our_dir in directories.ordered():
            try:
                for path in glob.glob("%s/*.s[ol]*" % our_dir):
                    file = os.path.basename(path)

                    # Index by filename
                    cache_i = cache.setdefault(file, set())
                    cache_i.add(path)

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        cache_i = cache.setdefault(library, set())
                        cache_i.add(path)
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname, set())
        for i in result:
            # we iterate through all found paths for library, since we may have
            # actually found multiple architectures or other library types that
            # may not load
            yield i


# Windows


class WindowsLibraryLoader(LibraryLoader):
    """Library loader for Microsoft Windows"""

    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll", "%s"]

    class Lookup(LibraryLoader.Lookup):
        """Lookup class for Windows libraries..."""

        def __init__(self, path):
            super(WindowsLibraryLoader.Lookup, self).__init__(path)
            self.access["stdcall"] = ctypes.windll.LoadLibrary(path)


# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin": DarwinLibraryLoader,
    "cygwin": WindowsLibraryLoader,
    "win32": WindowsLibraryLoader,
    "msys": WindowsLibraryLoader,
}

load_library = loaderclass.get(sys.platform, PosixLibraryLoader)()


def add_library_search_dirs(other_dirs):
    """
    Add libraries to search paths.
    If library paths are relative, convert them to absolute with respect to this
    file's directory
    """
    for path in other_dirs:
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        load_library.other_dirs.append(path)


del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries
_libs[r"C:\Prj\GitHub\ctypesgen\demo\simulinkDLL\test_ctrl_win64.dll"] = load_library(r"C:\Prj\GitHub\ctypesgen\demo\simulinkDLL\test_ctrl_win64.dll")

# 1 libraries
# End libraries

# No modules

uint16_T = c_ushort# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL/rtwtypes.h: 50

int32_T = c_int# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL/rtwtypes.h: 51

uint32_T = c_uint# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL/rtwtypes.h: 52

real32_T = c_float# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL/rtwtypes.h: 53

real_T = c_double# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL/rtwtypes.h: 60

boolean_T = c_ubyte# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL/rtwtypes.h: 62

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 127
class struct_tag_RTM_test_ctrl(Structure):
    def __init__(self):
        self.dwork = POINTER(D_Work_test_ctrl)()
        self.test_ctrl_InstP_ref = POINTER(InstP_test_ctrl)()
        super().__init__(
                         dwork=self.dwork,
                         test_ctrl_InstP_ref=self.test_ctrl_InstP_ref,
         )
    pass

RT_MODEL_test_ctrl = struct_tag_RTM_test_ctrl# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 26

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 34
class struct_anon_16(Structure):
    def __init__(self):
        self.diag1 = real32_T(0)
        self.diag2 = False
        super().__init__(
                         diag1=self.diag1,
                         diag2=self.diag2,
         )
    pass

struct_anon_16._fields_ = [
    ('diag1', real32_T),
    ('diag2', boolean_T),
]

TEST_CTRL_D_t = struct_anon_16# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 34

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 44
class struct_anon_17(Structure):
    def __init__(self):
        self.in1 = uint16_T(0)
        self.in2 = int32_T(0)
        super().__init__(
                         in1=self.in1,
                         in2=self.in2,
         )
    pass

struct_anon_17._fields_ = [
    ('in1', uint16_T),
    ('in2', int32_T),
]

InBus_t = struct_anon_17# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 44

enum_anon_18 = c_int# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 59

WORK_STATE_STREET = 0# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 59

WORK_STATE_FIELD = 1# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 59

WORK_STATE_HEADLAND = 2# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 59

WORK_STATE_OPEN_A_FIELD = 3# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 59

WORK_STATE_REVERSING = 4# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 59

WORK_STATE_ERROR_INDICATION = 14# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 59

WORK_STATE_NOT_AVAILABLE = 15# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 59

workingStateTypes = enum_anon_18# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 59

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 73
class struct_anon_19(Structure):
    def __init__(self):
        self.input1 = InBus_t()
        self.input2 = int32_T(0)
        self.input3 = real32_T(0)
        self.input4 = real_T(0)
        self.input5 = False
        self.input6 = workingStateTypes()
        super().__init__(
                         input1=self.input1,
                         input2=self.input2,
                         input3=self.input3,
                         input4=self.input4,
                         input5=self.input5,
                         input6=self.input6,
         )
    pass

struct_anon_19._fields_ = [
    ('input1', InBus_t),
    ('input2', int32_T),
    ('input3', real32_T),
    ('input4', real_T),
    ('input5', boolean_T),
    ('input6', workingStateTypes),
]

TEST_CTRL_U_t = struct_anon_19# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 73

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 83
class struct_anon_20(Structure):
    def __init__(self):
        self.output1 = real32_T(0)
        self.output2 = False
        super().__init__(
                         output1=self.output1,
                         output2=self.output2,
         )
    pass

struct_anon_20._fields_ = [
    ('output1', real32_T),
    ('output2', boolean_T),
]

TEST_CTRL_Y_t = struct_anon_20# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 83

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 94
class struct_anon_21(Structure):
    def __init__(self):
        self.ts = uint32_T(0)
        self.para1 = real32_T(0)
        self.para2 = real32_T(0)
        super().__init__(
                         ts=self.ts,
                         para1=self.para1,
                         para2=self.para2,
         )
    pass

struct_anon_21._fields_ = [
    ('ts', uint32_T),
    ('para1', real32_T),
    ('para2', real32_T),
]

TEST_CTRL_P_t = struct_anon_21# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 94

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 103
class struct_anon_22(Structure):
    def __init__(self):
        self.d = TEST_CTRL_D_t()
        self.DiscreteTimeIntegrator_DSTATE = real32_T(0)
        self.UnitDelay_DSTATE = real32_T(0)
        super().__init__(
                         d=self.d,
                         DiscreteTimeIntegrator_DSTATE=self.DiscreteTimeIntegrator_DSTATE,
                         UnitDelay_DSTATE=self.UnitDelay_DSTATE,
         )
    pass

struct_anon_22._fields_ = [
    ('d', TEST_CTRL_D_t),
    ('DiscreteTimeIntegrator_DSTATE', real32_T),
    ('UnitDelay_DSTATE', real32_T),
]

D_Work_test_ctrl = struct_anon_22# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 103

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 113
class struct_anon_23(Structure):
    def __init__(self):
        self.p = TEST_CTRL_P_t()
        super().__init__(
                         p=self.p,
         )
    pass

struct_anon_23._fields_ = [
    ('p', TEST_CTRL_P_t),
]

InstP_test_ctrl = struct_anon_23# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 113

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 118
class struct_anon_24(Structure):
    def __init__(self):
        self.U = TEST_CTRL_U_t()
        super().__init__(
                         U=self.U,
         )
    pass

struct_anon_24._fields_ = [
    ('U', TEST_CTRL_U_t),
]

ExternalInputs_test_ctrl = struct_anon_24# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 118

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 124
class struct_anon_25(Structure):
    def __init__(self):
        self.Y = TEST_CTRL_Y_t()
        self.D = TEST_CTRL_D_t()
        super().__init__(
                         Y=self.Y,
                         D=self.D,
         )
    pass

struct_anon_25._fields_ = [
    ('Y', TEST_CTRL_Y_t),
    ('D', TEST_CTRL_D_t),
]

ExternalOutputs_test_ctrl = struct_anon_25# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 124

struct_tag_RTM_test_ctrl._fields_ = [
    ('dwork', POINTER(D_Work_test_ctrl)),
    ('test_ctrl_InstP_ref', POINTER(InstP_test_ctrl)),
]

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 133
try:
    test_ctrl_rtZTEST_CTRL_U_t = (TEST_CTRL_U_t).in_dll(_libs[r"C:\Prj\GitHub\ctypesgen\demo\simulinkDLL\test_ctrl_win64.dll"], "test_ctrl_rtZTEST_CTRL_U_t")
except:
    pass

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 136
if _libs[r"C:\Prj\GitHub\ctypesgen\demo\simulinkDLL\test_ctrl_win64.dll"].has("test_ctrl_initialize", "cdecl"):
    test_ctrl_initialize = _libs[r"C:\Prj\GitHub\ctypesgen\demo\simulinkDLL\test_ctrl_win64.dll"].get("test_ctrl_initialize", "cdecl")
    test_ctrl_initialize.argtypes = [POINTER(RT_MODEL_test_ctrl), POINTER(ExternalInputs_test_ctrl), POINTER(ExternalOutputs_test_ctrl)]
    test_ctrl_initialize.restype = None

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 138
if _libs[r"C:\Prj\GitHub\ctypesgen\demo\simulinkDLL\test_ctrl_win64.dll"].has("test_ctrl_step", "cdecl"):
    test_ctrl_step = _libs[r"C:\Prj\GitHub\ctypesgen\demo\simulinkDLL\test_ctrl_win64.dll"].get("test_ctrl_step", "cdecl")
    test_ctrl_step.argtypes = [POINTER(RT_MODEL_test_ctrl), POINTER(ExternalInputs_test_ctrl), POINTER(ExternalOutputs_test_ctrl)]
    test_ctrl_step.restype = None

# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 140
if _libs[r"C:\Prj\GitHub\ctypesgen\demo\simulinkDLL\test_ctrl_win64.dll"].has("test_ctrl_terminate", "cdecl"):
    test_ctrl_terminate = _libs[r"C:\Prj\GitHub\ctypesgen\demo\simulinkDLL\test_ctrl_win64.dll"].get("test_ctrl_terminate", "cdecl")
    test_ctrl_terminate.argtypes = [POINTER(RT_MODEL_test_ctrl)]
    test_ctrl_terminate.restype = None

tag_RTM_test_ctrl = struct_tag_RTM_test_ctrl# C:\\Prj\\GitHub\\ctypesgen\\demo\\simulinkDLL\\test_ctrl.h: 127

# No inserted files

# No prefix-stripping

