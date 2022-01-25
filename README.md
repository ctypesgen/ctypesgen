                              ctypesgen
                              ---------

                  (c) Ctypesgen developers 2007-2022
                 https://github.com/ctypesgen/ctypesgen

_ctypesgen_ is a pure-python ctypes wrapper generator. It parses C header files
and creates a wrapper for libraries based on what it finds.

Preprocessor macros are handled in a manner consistent with typical C code.
Preprocessor macro functions are translated into Python functions that are then
made available to the user of the newly-generated Python wrapper library.

It can also output JSON, which can be used with Mork, which generates bindings
for Lua, using the alien module (which binds libffi to Lua).

## Documentation

See https://github.com/ctypesgen/ctypesgen/wiki for full documentation.

Run `ctypesgen --help` for full range of available options.

## Installation

_ctypesgen_ can be installed by `pip install ctypesgen`. It requires Python 3.7
to run.

## Basic Usage

This project automatically generates ctypes wrappers for header files written
in C.

For example, if you'd like to generate Neon bindings, you can do so using this
recipe (using a standard pip install):

```sh
ctypesgen -lneon /usr/local/include/neon/ne_*.h -o neon.py
```

Some libraries, such as APR, need special flags to compile. You can pass these
flags in on the command line.

For example:

```sh
FLAGS = `apr-1-config --cppflags --includes`
ctypesgen $FLAGS -llibapr-1.so $HOME/include/apr-1/apr*.h -o apr.py
```

Sometimes, libraries will depend on each other. You can specify these
dependencies using -mmodule, where module is the name of the dependency module.

Here's an example for apr_util:

```sh
ctypesgen $FLAGS -llibaprutil-1.so $HOME/include/apr-1/ap[ru]*.h \
	-mapr -o apr_util.py
```

If you want JSON output (e.g. for generating Lua bindings), use

```
--output-language=json
```

When outputting JSON, you will probably also want to use

```
--all-headers --builtin-symbols --no-stddef-types --no-gnu-types
--no-python-types
```

## Related Software of Interest

_libffi_ is a portable Foreign Function Interface library:
http://sources.redhat.com/libffi/

_Mork_, the friendly alien, can be found at:
https://github.com/rrthomas/mork

## License

_ctypesgen_ is distributed under the New (2-clause) BSD License:
http://www.opensource.org/licenses/bsd-license.php
