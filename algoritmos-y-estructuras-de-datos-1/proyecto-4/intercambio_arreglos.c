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

void intercambiar(int a[] , int tam , int i , int j){

  int aux;

  // Me tira warning si no utilizo la var tam
  tam = tam;

  aux = a[i];

  a[i] = a[j];

  a[j] = aux;

}

int main(void){

  int i , j ,arreglo[N];

  pedirArreglo(arreglo, N);

  printf("Que posiciones deseas intercambiar?\n");

  printf("i : ");
  scanf("%d" , &i);

  while(i < 0 || i > (N-1)){

    printf("Selecciono una posicion fuera del rango, elige nuevamente:\n");
    printf("i : ");
    scanf("%d", &i);

  }

  printf("j : ");
  scanf("%d" , &j);

  while (j < 0 || j > (N - 1)){

    printf("Selecciono una posicion fuera del rango, elige nuevamente:\n");
    printf("j : ");
    scanf("%d", &j);

  }

  intercambiar(arreglo , N , i , j);

  
  printf("El arreglo final es:\n [");

  for (i = 0 ; i < N-1 ; i++){

    printf("%d," , arreglo[i]);
    
  }

  printf("%d]\n" , arreglo[N-1]);
  
  return 0;
}
