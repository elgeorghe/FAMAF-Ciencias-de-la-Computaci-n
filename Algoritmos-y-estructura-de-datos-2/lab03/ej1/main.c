/**
 ** Para poder compilar los archivos usamos la sig linea en la consola
 * gcc -Wall -Werror -Wextra -pedantic -std=c99 main.c -o main
 * ./main
 *
 * * Y para utilizar el debugger
 * gcc -Wall -Werror -Wextra -pedantic -std=c99 -g miarchivo.c -o miprograma
 * gdb ./miprograma
 *
*/

/*
  @file main.c
  @brief Main program function implementation
*/
#include <stdio.h>
#include <stdlib.h>

/** @brief structure which represent a person */
typedef struct _person {

    int age;
    char name_initial;

} person_t;

/**
 * @brief Main program function
 *
 * @return EXIT_SUCCESS when programs executes correctly, EXIT_FAILURE otherwise
 */
int main(void) {

    int x = 1;
    person_t m = {90, 'M'};
    int a[] = {0, 1, 2, 3};

    /*
      Mi codigo agregado 
    
      Inicializo mis punteros en NULL (No apuntan a nada)
      Solo puedo utilizar 2, asique uno sera un puntero de int y otro un puntero de estrucutra person_t
    */

    int *puntero_de_int = NULL;
    person_t *puntero_de_struct = NULL;    

    // Hago que el puntero de int apunte a la direccion donde esta guardada "x"
    puntero_de_int = &x;

    // Ahora le digo que modifique el valor guardado en la direccion del puntero
    *puntero_de_int = 9;

    // Hago lo mismo que recien pero ahora con la estructura "m"
    puntero_de_struct = &m;

    // En lugar de usar el foramto *q.age , se usa q->age
    puntero_de_struct -> age = 100 ;
    puntero_de_struct -> name_initial = 'F';

    // Y por ultimo tomo la direccion del valor en la posicion 1 del arreglo a y lo modifico
    puntero_de_int = &a[1];
    *puntero_de_int = 42;

    /*
      Fin Codigo Agregado
    */

    printf("x = %d\n", x);
    printf("m = (%d, %c)\n", m.age, m.name_initial);
    printf("a[1] = %d\n", a[1]);

    return EXIT_SUCCESS;
}

