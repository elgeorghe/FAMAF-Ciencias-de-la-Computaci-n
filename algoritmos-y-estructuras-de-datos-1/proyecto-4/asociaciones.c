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
typedef char clave_t;
typedef int valor_t;

// Estructura de asoc
typedef struct{

  clave_t clave;
  valor_t valor;

} asoc;

void pedirArreglo(asoc a[], int n_max){

  int x, i = 0;
  char c;

  asoc dupla;
  dupla.clave = 0;
  dupla.valor = 0;

  while (i < n_max){

    printf("Elige una clave y valor separados por un espacio:\n");
    scanf(" %c %d", &c , &x);

    dupla.clave = c;
    dupla.valor = x;

    a[i] = dupla;

    i++;
  }
}

bool asoc_existe(asoc a[] , int tam , clave_t c){

  int i = 0;

  while (i < tam){
    
    if (a[i].clave == c){

      return true;
      
    }

    i ++;
  }

  return false;
}

int main(void){

  asoc arreglo[N];
  char clave ;
  bool temp;

  pedirArreglo(arreglo, N);

  printf("Que clave quiere buscar?:\n");
  scanf(" %c", &clave);
  
  temp = asoc_existe(arreglo , N , clave);

  if (temp == true){

    printf("La clave existe\n");

  } else {

    printf("La clave no existe\n");

  }

  return 0;
}