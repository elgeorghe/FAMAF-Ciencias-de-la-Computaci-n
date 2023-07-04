
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

int pedirEntero(void){

  int x;

  printf("Ingresar un numero entero:\n");
  scanf("%d", &x);

  return x;
}

void imprimeEntero(int x){

  printf("El entero es %d\n", x);
  
}

int main(void){  
  
  imprimeEntero(pedirEntero());
 
  return 0;
}