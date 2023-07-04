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

  int x, y;
  
  printf("Valor de x:\n");
  scanf("%d", &x);

  printf("Valor de y:\n");
  scanf("%d", &y);

  x = x + y;
  y = y + y;

  printf("Los nuevos valores de x e y son:\n x=%d ; y=%d \n", x, y);

  /*
 x=5 ; y=3  => x=8 ; y=6
 x=2 ; y=4  => x=6 ; y=8
 x=1 ; y=8  => x=9 ; y=16
 */

  return 0;
}