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

void imprimeHola(void){

  printf("Hola\n");

}

void imprimeChau(void){

  printf("Chau\n");
  
}

int main(void){

  imprimeHola();
  imprimeHola();
  imprimeChau();
  imprimeChau();

  return 0;
}