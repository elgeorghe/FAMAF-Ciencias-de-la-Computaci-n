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

int main(void){

  int x, y, z, m;  

  x = pedirEntero();
  y = pedirEntero();
  z = pedirEntero();
  m = pedirEntero();

  if (x < y){

    m = x;

  } else {

    m = y;

  }

  if (m >= z){

    m = z;

  }

  // Una ventaja es el ahorrarse el tener que escribir printf y scanf
  // Podria escribir la funcion que calcule el min directo y hacer que la funcion main la llame

  printf("El minimo entre x, y, z es:\n min = %d\n", m);

  return 0;
}
