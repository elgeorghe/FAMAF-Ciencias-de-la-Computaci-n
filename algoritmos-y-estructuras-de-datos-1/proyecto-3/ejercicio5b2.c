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

int main(void){

  int i, x, temp;
  bool res;

  printf("Valor de x:\n");
  scanf("%d", &x);

  printf("Valor de i:\n");
  scanf("%d", &i);

  printf("Ingrese un bool: 0 para false, 1 para true:\n");
  scanf("%d", &temp);

  res = temp;
  i = 2;
  res = 1;

  while (i < x && res){

    res = res && (x % i != 0);
    i = i + 1;

  }

  printf("Los valores de x, i, res son:\n x = %d ; i = %d ; res = %d\n", x, i, res);

  /*
  x=5 ; i=2 ; res=True
  =>
  x=5 ; i=3 ; res=True
  =>
  x=5 ; i=4 ; res=True
  =>
  x=5 ; i=5 ; res=True  
  */

  return 0;
}