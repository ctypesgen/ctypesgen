                              ctypesgen
                              ---------

                  (c) Ctypesgen developers 2007-2021
                 https://github.com/davidjamesca/ctypesgen

ctypesgen is a pure-python ctypes wrapper generator. It can also
output JSON, which can be used with Mork, which generates bindings for
Lua, using the alien module (which binds libffi to Lua).

Documentation
-------------

See https://github.com/davidjamesca/ctypesgen/wiki for full documentation.

Basic Usage
-----------

This project automatically generates ctypes wrappers for header files written
in C.

For example, if you'd like to generate Neon bindings, you can do so using this
recipe:

	$ python ctypesgen.py -lneon /usr/local/include/neon/ne_*.h -o neon.py

Some libraries, such as APR, need special flags to compile. You can pass these
flags in on the command line.

For example:

	$ FLAGS = `apr-1-config --cppflags --includes`
	$ python ctypesgen.py $FLAGS -llibapr-1.so $HOME/include/apr-1/apr*.h -o apr.py

Sometimes, libraries will depend on each other. You can specify these
dependencies using -mmodule, where module is the name of the dependency module.

Here's an example for apr_util:

	$ python ctypesgen.py $FLAGS -llibaprutil-1.so $HOME/include/apr-1/ap[ru]*.h \
	-mapr -o apr_util.py


If you want JSON output (e.g. for generating Lua bindings), use

	--output-language=json

When outputting JSON, you will probably also want to use

	--all-headers --builtin-symbols --no-stddef-types --no-gnu-types
	--no-python-types

License
-------

ctypesgen is distributed under the New (2-clause) BSD License:
http://www.opensource.org/licenses/bsd-license.php

libffi is a portable Foreign Function Interface library:
http://sources.redhat.com/libffi/

Mork, the friendly alien, can be found at:
https://github.com/rrthomas/mork


Versioning
----------

Versioning within ctypesgen follows these general rules:

* Versions are all defined with specific reference to a commit that is relative
  to a Git tag.
* Versions numbers include enough information to find the exact commit that
  represents the version release.
* All tags should follow the format of:  ctypesgen-x.y.z
    * x : Major revision with major differences of capabilities as compared to
          other major revisions.  The definition of "major capabilities" is a
          somewhat subjective concept, dependent on the developers.
    * y : Minor revision with incompatible differences of interfaces as compared
          to earlier revisions.  Interfaces that are considered to impact the
          minor revision number are external interfaces such as the command line
          or perhaps python version support.
    * z : Micro revision indicating a general acceptance of multiple patches
          since last tag. This number may be used to help mark minor development
          milestones.

By using the Git command ‘git describe‘, a unique identifier of the full version
string can be shown as:

  * ctypesgen-x.y.z[-n-g*sha1*]
    where [-n-g*sha1*] shows up *automatically* if changes have been made since
    the last tag
  * n : Indicates the number of commits since the last tag
  * g*sha1*: Indicates the abreviated SHA1 hash of the latest commit

Thus, the version *1.0.0-2* means that the last tag before that version was
*ctypesgen-1.0.0* and the version *1.0.0-2* is exactly 2 commits after the tag
*ctypesgen-1.0.0*.

To re-baseline the [-n-g*sha1*] portion showing up in "git describe" (i.e.
remove it until another commit is added), we simply add another tag following
the *ctypesgen-x.y.z* format.
