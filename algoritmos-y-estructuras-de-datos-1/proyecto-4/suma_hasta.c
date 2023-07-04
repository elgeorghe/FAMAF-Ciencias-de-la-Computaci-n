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


int suma_hasta(int N){

  int i;

  i = (N * (N + 1)) / 2;
  
  return i;
}

int main(void){

  int N,i;

  printf("Ingrese N:\n");
  scanf("%d", &N);
  
  if (N >= 0){

    i = suma_hasta(N);

    printf("La suma hasta N es: %d\n", i);

  } else {

    printf("Error\n");

  }

  return 0;
}