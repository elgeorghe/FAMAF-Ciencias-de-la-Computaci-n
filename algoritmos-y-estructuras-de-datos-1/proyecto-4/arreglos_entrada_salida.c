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
#include <stdbool.h>

void pedirArreglo(int a[] , int n_max){

  int x , i = 0;

  while (i < n_max){

    printf("Valor para la posicion %d:\n" , i);
    scanf("%d", &x);

    a[i] = x;
    i ++;

  }
}

void imprimeArreglo(int a[] , int n_max){

  int i = 0;

  while (i < n_max){

    printf("El valor en la posicion %d es: %d\n", i , a[i]);    
    i++;

  }
}

int main(void){

  int n_max;

  printf("Tamaño del arreglo:\n");
  scanf("%d" , &n_max);

  int arreglo[n_max];

  pedirArreglo(arreglo , n_max);

  imprimeArreglo(arreglo , n_max);

  return 0;
}