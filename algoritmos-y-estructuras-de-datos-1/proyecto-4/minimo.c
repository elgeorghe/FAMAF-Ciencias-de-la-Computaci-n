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

int minimo(int x, int y){

  int i = 0;

  if (x < y){

    i = x;

  } else {

    i = y;

  }

  return i;
}

int main(void){

  int x, y, i;

  printf("Valor de x:\n");
  scanf("%d", &x);

  printf("Valor de y:\n");
  scanf("%d", &y);

  assert(true);

  i = minimo(x, y);

  assert(i == x || i == y);

  printf("El minimo es:\n i = %d\n", i);

  return 0;
}