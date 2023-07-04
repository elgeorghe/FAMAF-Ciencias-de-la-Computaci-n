/**
 * * Para este ejercicio se pide que se compile de la sig manera:
 * gcc -Wall -Werror -pedantic -std=c99 proc1.c -o abs1
 * ./abs1
*/

#include <stdlib.h>
#include <stdio.h>

void absolute(int x, int y) {
    
    y = x >= 0? x : -x ;
    
}

int main(void) {

    int a=0, res=0;
    
    a = -10;
    
    absolute(a,res);

    printf("%d\n" , res);

    res = 0;

    return EXIT_SUCCESS;
}

/*
    Por pantalla se muestra el valor 0. No coincide con el programa del teorico porque deberia devolver 10.
*/