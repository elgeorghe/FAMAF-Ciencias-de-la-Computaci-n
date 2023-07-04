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
#include <limits.h>
#define N 5

void pedirArreglo(float a[], int n_max){

  float x;
  int i = 0;

  while (i < n_max){

    printf("Valor para la posicion %d:\n", i);
    scanf("%f", &x);

    a[i] = x;
    i ++;

  }
}

// Estructura de datos_t
typedef struct{

  float maximo;
  float minimo;
  float promedio;

} datos_t;

datos_t stats(float a[] , int tam){

  int i = 0 ;
  float sum = 0;

  datos_t trio;
  trio.maximo = INT_MIN;
  trio.minimo = INT_MAX;
  trio.promedio = 0;

  while (i < tam){

    if (a[i] >= trio.maximo){

      trio.maximo = a[i];
    }

    if (a[i] <= trio.minimo){

      trio.minimo = a[i];
    }

    sum += a[i];

    i ++;

  }

  trio.promedio = sum / N;

  return trio;
}

int main(void){

  float arreglo[N] , max = 0 , min = 0 , prom = 0;

  pedirArreglo(arreglo, N);

  datos_t trio_nuevo = stats(arreglo , N);

  max = trio_nuevo.maximo;
  min = trio_nuevo.minimo;
  prom = trio_nuevo.promedio;

  printf("El maximo, minimo y promedio son:\n maximo: %f ; minimo: %f ; promedio: %f\n", max, min, prom);

  return 0;
}