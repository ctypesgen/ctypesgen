import sys
import functools
import ctypes
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


# ~POINTER~


if sys.version_info < (3, 8):
    # NOTE alternatively, we could write our own cached property backport with python's descriptor protocol
    def cached_property(func):
        return property( functools.lru_cache(maxsize=1)(func) )
else:
    cached_property = functools.cached_property


DEFAULT_ENCODING = "utf-8"

class _wraps_c_char_p:
    
    def __init__(self, ptr):
        self.ptr = ptr
    
    @cached_property
    def raw(self):
        return self.ptr.value
    
    @cached_property
    def decoded(self):
        if self.raw is None:
            raise RuntimeError("Null pointer cannot be decoded")
        return self.raw.decode(DEFAULT_ENCODING)
    
    def __str__(self):
        return self.decoded
    
    def __getattr__(self, attr):
        return getattr(self.decoded, attr)
    
    def __eq__(self, other):
        if isinstance(other, str):
            return self.decoded == other
        else:
            return self.raw == other


class String (ctypes.c_char_p):
    
    @classmethod
    def _check_retval_(cls, result):
        return _wraps_c_char_p(result)
    
    @classmethod
    def from_param(cls, obj):
        if isinstance(obj, str):
            obj = obj.encode(DEFAULT_ENCODING)
        return super().from_param(obj)



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
