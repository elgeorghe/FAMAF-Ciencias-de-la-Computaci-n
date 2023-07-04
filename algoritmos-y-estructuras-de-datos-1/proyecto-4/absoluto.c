/**
 ** Para poder compilar los archivos usamos la sig linea en la consola
 * gcc -Wall -Wextra -std=c99 miarchivo.c -o miprograma
 * ./miprograma
 *
 * * Y para utilizar el debugger
 * gcc -Wall -Wextra -std=c99 -g miarchivo.c -o miprograma
 * gdb ./miprograma
 *
 */

#include <stdio.h>
#include <stdbool.h>
#include <assert.h>

int valorabsoluto(int x){

  int i = 0;

  if (x < 0){

    i = -x;

  } else {

    i = x;

  }

  return i;
}

int main(void){

  int x,i;

  printf("Ingrese el valor de x:\n");
  scanf("%d", &x);

  assert(true);

  i = valorabsoluto(x);

  assert(i >= 0);

  printf("El valor absoluto es:\n i = %d\n", i);

  return 0;
}