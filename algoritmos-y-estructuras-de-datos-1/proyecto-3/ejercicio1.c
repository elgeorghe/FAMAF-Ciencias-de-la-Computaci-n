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

  int x, y, z, i;

  printf("Valor de x:\n");
  scanf("%d", &x);

  printf("Valor de y:\n");
  scanf("%d", &y);

  printf("Valor de z:\n");
  scanf("%d", &z);

  printf("Las respuestas son:\n");

  i = x + y + 1;
  printf("x + y + 1 = %d\n", i);

  i = z * z + y * 45 - 15 * x;
  printf("z * z + y * 45 - 15 * x = %d\n", i);

  i = y - 2 == (x * 3 + 1) % 5;
  printf("y - 2 == (x * 3 + 1) mod 5 == %d (el 0 es False y 1 True)\n", i);

  i = y / 2 * x;
  printf("y / 2 * x = %d\n", i);

  i = y < x * z;
  printf("y < x * z = %d (el 0 es False y 1 True)\n", i);

  /*
  Para x=7 ; y=3 ; z=5 los resultados son:
  - 11
  - 55
  - 0 (False)
  - 7
  - 1 (True)
  Para x=1 ; y=10 ; z=8 los resultados son:
  - 12
  - 499
  - 0 (False)
  - 5
  - 0 (False)
  */

  // El tipo en C de la ultima expresion es Int, ya que no hay Booleanos

  return 0;
}