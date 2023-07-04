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

int sumatoria(int a[], int tam){

  int sum = 0 , i = 0;

  while (i < tam){
   
    sum += a[i];    
    i ++;

  }

  return sum;
}

int main(void){  

  int sumtotal , arreglo[N];

  pedirArreglo(arreglo, N);

  sumtotal = sumatoria(arreglo , N);

  printf("La suma de los elementos es: %d\n" , sumtotal);  

  return 0;
}