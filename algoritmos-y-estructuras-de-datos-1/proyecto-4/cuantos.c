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

// Estructura de comp_t
typedef struct{

  int menores;
  int iguales;
  int mayores;
  
} comp_t;

comp_t cuantos(int a[] , int tam , int elem){

  int i = 0;

  comp_t trio;
  trio.menores = 0;
  trio.iguales = 0;
  trio.mayores = 0;

  while (i < tam){

    if (a[i] > elem){

      trio.mayores ++;

    } else {

      if (a[i] < elem){

        trio.menores ++;

      } else {

        trio.iguales ++;

      }    
    }

    i ++;
  }

  return trio;
}

int main(void){

  int x, menores, mayores , iguales, arreglo[N];

  pedirArreglo(arreglo, N);

  printf("Elige valor de x:\n");
  scanf("%d" , &x);

  comp_t trio_final = cuantos(arreglo , N , x);

  menores = trio_final.menores;
  iguales = trio_final.iguales;
  mayores = trio_final.mayores;

  printf("La cantidad de elementos menores, iguales y mayores a %d son:\n menores: %d ; iguales: %d ; mayores: %d\n" , x , menores , iguales , mayores);  

  return 0;
}