/*
  @file main.c
  @brief Main program function implementation
*/

/**
 * * Para poder compilar los archivos usamos la sig linea en la consola
 * gcc -Wall -Werror -Wextra -pedantic -std=c99 -c helpers.c sort.c main.c
 * gcc -Wall -Werror -Wextra -pedantic -std=c99 helpers.o sort.o main.o -o mysort
 * ./mysort ../input/atp-players2022.in
*/

/* First, the standard lib includes, alphabetically ordered */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>


/* Then, this project's includes, alphabetically ordered */
#include "helpers.h"
#include "sort.h"
#include "player.h"

#define MAX_PLAYERS 5000

/**
 * @brief print usage help
 * @param[in] program_name Executable name
 */
void print_help(char *program_name) {
    /* Print the usage help of this program. */
    printf("Usage: %s <input file path>\n\n"
           "Sort an array given in a file in disk.\n"
           "\n"
           "The input file must have the following format:\n"
           " * Each line must contain the name of a player"
           " without spaces followed by a three-letter country"
           " code, the rank of the player, his age, his atp points"
           " and the number of tournaments played during the year.\n"
           " * Values must be separated by one or more spaces.\n"
           " * Numeric values must be natural numbers.\n\n",
           program_name);
}

/**
 * @brief reads file path from command line
 *
 * @param[in] argc amount of command line arguments
 * @param[in] argv command line arguments
 *
 * @return An string containing read filepath
 */
char *parse_filepath(int argc, char *argv[]) {
    /* Parse the filepath given by command line argument. */
    char *result = NULL;

    if (argc < 2) {
        print_help(argv[0]);
        exit(EXIT_FAILURE);
    }

    result = argv[1];

    return (result);
}

/**
 * @brief Main program function
 *
 * @param[in] argc amount of command line arguments
 * @param[in] argv command line arguments
 *
 * @return EXIT_SUCCESS when programs executes correctly, EXIT_FAILURE otherwise
 */
int main(int argc, char *argv[]) {
    char *filepath = NULL;
    player_t atp[MAX_PLAYERS];

    /* parse the filepath given in command line arguments */
    filepath = parse_filepath(argc, argv);

    /* parse the file to load de players */
    unsigned int length = process_file(filepath, atp);

    /* create a copy of the array, to do some checks later */
    player_t copy[MAX_PLAYERS];
    array_copy(copy, atp, length);

    /* enable statistics for cpu utilization */
    {
        clock_t start, end;

        start = clock();

        /* do the actual sorting */
        sort(atp, length);

        end = clock();

        /* cpu_time used to sort the array */
        double used_cpu_time = ((double) (end - start)) / CLOCKS_PER_SEC;

        /* show the ordered array in the screen */
        atp_dump(atp, length);

        /* show the cpu time in seconds used to sort the array */
        printf("\ncpu time used to sort the array: %f seconds.\n", used_cpu_time);
    }

    /* check if it is sorted */
    assert(array_is_sorted(atp, length));

    /* check if it is a permutation of original */
    assert(array_is_permutation_of(copy, atp, length));

    destroy(atp, length);

    return (EXIT_SUCCESS);
}

/*
    Respuestas:

    1 - La funcion con punteros es mas rapida

        *ej5: cpu time used to sort the array: 0.035737 seconds. 

        *ej6: cpu time used to sort the array: 0.009463 seconds

    2 - Los punteros crean código eficiente y rápido ya que están más cerca del hardware. Esto significa que el compilador puede traducir más fácilmente
        la operación en código máquina. El “overhead” es mucho menor al utilizar punteros a diferencia de la cantidad de “overhead” que podría presentarse al utilizar otros operadores. Esto sin duda, mejora la administración de memoria de cualquier dispositivo como puede ser un microcontrolador.

        Ahora con mis palabras, el puntero nos da una ruta/direccion mas directa, por ende el acceso a la memoria es mas veloz.

    3 - La funcion destroy() por como esta implementada se encarga de liberar el bloque de memoria donde esta apuntando el puntero y luego hace que el
        puntero apunte a NULL, que es lo mismo que decir que no apunta a nada.
        Si no se realizamos esto entonces podriamos tener memory leak.

*/