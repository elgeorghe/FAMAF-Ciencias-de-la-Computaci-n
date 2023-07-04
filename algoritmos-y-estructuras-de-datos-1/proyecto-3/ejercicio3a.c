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

  int x;  

  printf("Valor de x:\n");
  scanf("%d", &x);

  x = 5;

  printf("El nuevo valor de x es: %d\n", x); 

  /*
  x=7  => x=5
  x=4  => x=5
  x=3  => x=5  
  */

  return 0;

}