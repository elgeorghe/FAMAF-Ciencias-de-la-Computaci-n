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

  int i, x, y;  

  printf("Valor de x:\n");
  scanf("%d", &x);

  printf("Valor de y:\n");
  scanf("%d", &y);

  printf("Valor de i:\n");
  scanf("%d", &i);

  i = 0;

  while (x >= y){

    x = x - y;
    i = i + 1;

  }

  printf("Los valores de x, y, i son:\n x = %d ; y = %d ; i = %d\n", x, y, i);

  /*
  x=13 ; y=3 ; i=0
  =>
  x=10 ; y=3 ; i=1
  =>
  x=7 ; y=3 ; i=2
  =>
  x=4 ; y=3 ; i=3
  =>
  x=1 ; y=3 ; i=4
  */

  return 0;
}