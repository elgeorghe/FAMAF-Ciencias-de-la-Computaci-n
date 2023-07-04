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

bool pedirBooleano(void){

  bool x;
  int temp;

  printf("Ingrese un bool: 0 para false, 1 para true:\n");
  scanf("%d", &temp);

  x = temp;

  return x;
}

void imprimeBooleano(bool x){

  if (x == true){

    printf("Verdadero\n");

  } else {

    printf("Falso\n");
    
  }
}

int main(void){
  
  imprimeBooleano(pedirBooleano());

  return 0;
}