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

int main(void){

  int x, y, z, b, w, i;

  printf("Valor de x:\n");
  scanf("%d", &x);

  printf("Valor de y:\n");
  scanf("%d", &y);

  printf("Valor de z:\n");
  scanf("%d", &z);

  printf("Ingrese un bool: 0 para false, 1 para true:\n");
  scanf("%d", &b);

  printf("Ingrese un bool: 0 para false, 1 para true:\n");
  scanf("%d", &w);

  printf("Las respuestas son:\n");

  i = (x % 4 == 0);
  printf("x mod 4 == 0 = %d (el 0 es False y 1 True)\n", i);

  i = ((x + y == 0) && (y - x == (-1) * z));
  printf("(x + y == 0) && (y - x == (-1) * z) = %d (el 0 es False y 1 True)\n", i);

  i = !(b && w);
  printf("not b && w = %d (el 0 es False y 1 True)\n", i);

  // Los valores que lo resuelven son x=4  ; y=(-4) ; z=8 ; b=True; w=True

  return 0;
}