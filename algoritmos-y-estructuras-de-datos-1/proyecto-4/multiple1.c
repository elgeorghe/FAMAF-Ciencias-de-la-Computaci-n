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

int main(void){

  int x, y, aux, X, Y;

  printf("Valor de x:\n");
  scanf("%d", &x);

  printf("Valor de y:\n");
  scanf("%d", &y);

  // Variables para comparacion final
  X = x;
  Y = y;

  assert(x == X && y == Y);

  // Cambio de Var
  aux = x;

  x = x + 1;

  y = aux + y;

  assert(x == X + 1 && y == X + Y);

  printf("Las variables quedan:\n x=%d ; y=%d\n", x, y);

  return 0;
}