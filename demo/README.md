Small Demonstration of Ctypesgen
================================

This little demonstration was originally written by developer clach04 (when this
was still residing on code.google.com).  This example shows how bindings for a
very simple c-library and associated header can be quickly generated using
Ctypesgen and accessed by a Python program.

This resulting bindings will work for Python2 as well as Python3.

Most of the instructions are included in the top of the various files, but a
summary is given here.


Steps:
----------
 1. Compile the shared c-library

      $ gcc -fPIC -shared -o demolib.so demolib.c

 2. (Re)Generate the bindings (or you can just try the bindings that were
    already generated and saved in this directory):

      $ ../run.py -o pydemolib.py -l demolib.so demolib.h

 3. Run the app that uses these newly generated bindings

      $ ./demoapp.py

    The results of this execution should give

>      a 1
>      b 2
>      result 3

 4. You can also try executing the same code completely from a c-program

    - Compile test code:

        $ gcc -o demoapp demoapp.c  demolib.c demolib.h

    - Execute:

        $ ./demoapp

    - Observe the same results as before:

>        a 1
>        b 2
>        result 3
