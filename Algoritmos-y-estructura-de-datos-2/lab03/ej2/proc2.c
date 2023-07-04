/**
 * * Para este ejercicio se pide que se compile de la sig manera:
 * gcc -Wall -Werror -Wextra -pedantic -std=c99 proc2.c -o abs2
 * ./abs2
*/

#include <stdlib.h>
#include <stdio.h>

void absolute(int x, int *y) {

    // En este caso estamos utilizando un puntero de int

    *y = x >= 0? x : -x ;
    
}

int main(void) {

    int a=0, res=0;  // No modificar esta declaración
    
    // Como ahora estoy utilizando punteros, declaro uno y le doy la direccion de res
    int *valor = NULL;
    valor = &res;

    a = -10;
    
    // Ahora le doy a absolute el puntero que apunta a la direccion de res y asi modificarlo
    absolute(a,valor);

    printf("%d\n" , res);

    res = 0;

    return EXIT_SUCCESS;
}

/*
    Respuestas:

    1 - El parametro int *y es de tipo in. Porque lo que hacemos es leer la direccion pero nunca modifcamos dicho valor. 
        Lo que modifcamos es el valor dentro de esa direccion.
    
    2 - En C los tipos de los parametros en las funciones son de in. Esto lo podemos ver en el proc1, porque si 
        fuesen de out o in/out el programa funcionaria sin problema.

*/