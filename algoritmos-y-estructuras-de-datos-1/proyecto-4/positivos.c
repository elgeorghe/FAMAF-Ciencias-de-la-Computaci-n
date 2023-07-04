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

bool existe_positivo(int a[] , int tam){

  int i = 0;
  
  while (i < tam){

    if (a[i] > 0){

      return true;

    } else {

      i++;

    }    
  }

  return false;

}

bool todos_positivo(int a[], int tam){

  int i = 0;

  while (i < tam){

    if (a[i] > 0){

      i++;

    } else {

      return false;

    }
  }

  return true;

}

int main(void){

  int x , arreglo[N];
  bool valor;

  pedirArreglo(arreglo, N);

  printf("Ingrese 1 para saber si algun elemento es positivo o 2 para saber si todos son positivos:\n");
  scanf("%d" , &x);

  if (x == 1) {

    valor = existe_positivo(arreglo , N);

    if (valor == true){

      printf("Verdadero\n");

    } else {

      printf("Falso\n");

    }

  } else {

    valor = todos_positivo(arreglo, N);

    if (valor == true){

      printf("Verdadero\n");

    } else {

      printf("Falso\n");

    }
  } 

  return 0;
}
