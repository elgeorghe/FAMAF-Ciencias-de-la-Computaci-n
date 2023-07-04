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
#include <assert.h>

void holaHasta(int n){

  int i = 0;

  while (i < n){

    printf("Hola\n");
    i++;

  }
}

void flagpositivo(int n){

  assert(n > 0);
  
}

int main(void){

  int n;  

  printf("Cuantos Holas queres imprimir?\n");
  scanf("%d", &n);

  flagpositivo (n);

  holaHasta(n);
  
  return 0;
  } 
