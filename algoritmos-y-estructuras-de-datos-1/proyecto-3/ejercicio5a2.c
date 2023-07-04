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

  int i;
  
  printf("Valor de i:\n");
  scanf("%d", &i);

  while (i != 0){

    i = 0;

  }

  printf("El valor de i es:\n i = %d\n", i); 

  return 0;
}