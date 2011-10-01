/*
** Trivial ctypesgen demo library
**  from http://code.google.com/p/ctypesgen

Dumb manual build with:


    gcc -fPIC -c demolib.c
    gcc -shared -o demolib.so demolib.o

    gcc -fPIC -shared -o demolib.so demolib.c

*/

#include "demolib.h"

int trivial_add(int a, int b)
{
    return a + b;
}
