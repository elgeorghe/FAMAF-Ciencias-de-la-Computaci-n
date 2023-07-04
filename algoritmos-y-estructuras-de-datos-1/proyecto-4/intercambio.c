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

  int x,y,aux,a,b;

  printf("Valor de x:\n");
  scanf("%d", &x);

  printf("Valor de y:\n");
  scanf("%d",&y);

  assert(true);

  // Variables para comparacion final
  a = x;
  b = y;

  // Cambio de Var
  aux = x;

  x = y;

  y = aux;

  assert( x == b && y == a);

  printf("Las variables quedan:\n x=%d ; y=%d\n", x, y);

  return 0;
}