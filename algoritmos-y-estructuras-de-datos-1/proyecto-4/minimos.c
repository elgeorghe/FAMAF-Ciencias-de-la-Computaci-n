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

void pedirArreglo(int a[], int n_max){

  int x, i = 0;

  while (i < n_max){

    printf("Valor para la posicion %d:\n", i);
    scanf("%d", &x);

    a[i] = x;
    i++;

  }
}

int minimo_pares(int a[] , int tam){

  int min_pares = INT_MAX , i = 0;

  while (i < tam){
    
    if (a[i] < min_pares){

      min_pares = a[i];

    }    

    i += 2; 
  }

  return min_pares;
}

int minimo_impares(int a[] , int tam){

  int min_impares = INT_MAX, i = 1;

  while (i < tam){

    if (a[i] < min_impares){

      min_impares = a[i];

    }

    i += 2;
  }

  return min_impares;
}

int main(void){

  int min_pares , min_impares , arreglo[N];

  pedirArreglo(arreglo, N);

  min_pares = minimo_pares(arreglo , N);
  min_impares = minimo_impares(arreglo , N);

  if (min_pares <= min_impares){

    printf("El minimo del arreglo es:\n min = %d\n" , min_pares);

  } else {

    printf("El minimo del arreglo es:\n min = %d\n", min_impares);

  }
  
  return 0;
}
