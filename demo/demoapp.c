/*
** Trivial ctypesgen demo library consumer
**  from http://code.google.com/p/ctypesgen
**
** This demoapp it self is not useful, it is a sanity check for the library.
**
**  Build static:   cc -o demoapp demoapp.c  demolib.c  demolib.h
**
*/


#include <stdlib.h>
#include <stdio.h>

#include "demolib.h"

int main(int argc, char **argv)
{
    int a = 1;
    int b = 2;
    int result = 0;

    result = trivial_add(a, b);
    printf("a %d\n", a);
    printf("b %d\n", b);
    printf("result %d\n", result);
}
