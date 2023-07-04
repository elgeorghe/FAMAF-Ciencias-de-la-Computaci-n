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

  int x, y, z, xaux, yaux, X, Y, Z;

  printf("Valor de x:\n");
  scanf("%d", &x);

  printf("Valor de y:\n");
  scanf("%d", &y);

  printf("Valor de z:\n");
  scanf("%d", &z);

  // Variables para comparacion final
  X = x;
  Y = y;
  Z = z;

  assert(x == X && y == Y && z == Z);

  // Cambio de Var
  xaux = x;
  yaux = y;

  x = y;
  
  y = y + xaux + z;

  z = yaux + xaux;

  assert(x == Y && y == Y + X + Z && z == Y + X);

  printf("Las variables quedan:\n x=%d ; y=%d ; z=%d\n", x, y, z);

  return 0;
}