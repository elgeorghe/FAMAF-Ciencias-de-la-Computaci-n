/**
 * * Para poder compilar los archivos usamos la sig linea en la consola
 * gcc -Wall -Werror -Wextra -pedantic -std=c99 -c funciones_extras.c
 * gcc -Wall -Werror -Wextra -pedantic -std=c99 -c main.c
 * gcc -Wall -Werror -Wextra -pedantic -std=c99 funciones_extras.o main.o -o readprhase
 * ./readprhase phrase-basic.in
*/

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

// Incluyo la libreria de funcions extras
#include "funciones_extras.h"

#define MAX_SIZE 1000

// Funcion para imprimr el arreglo final, igual al de labs anteriores
static void dump(char a[], unsigned int length) {

    printf("\"");

    for (unsigned int j=0u; j < length; j++) {

        printf("%c", a[j]);

    }

    printf("\"");
    printf("\n\n");
}


int main(int argc, char *argv[]) {

    char *filepath = NULL;

    // Uso esta funcion del lab01 que me devuelve la direccion del archivo a leer
    filepath = parse_filepath(argc, argv);

    unsigned int indexes[MAX_SIZE];
    char letters[MAX_SIZE];
    char sorted[MAX_SIZE];
    unsigned int length = 0u; 

    length = data_from_file(filepath , indexes , letters , MAX_SIZE);

    sort(sorted , indexes , letters , length);

    dump(sorted, length);

    return EXIT_SUCCESS;
}

