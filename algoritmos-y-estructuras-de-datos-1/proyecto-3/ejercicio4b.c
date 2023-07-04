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

  int x, y, z, m;

  printf("Valor de x:\n");
  scanf("%d", &x);

  printf("Valor de y:\n");
  scanf("%d", &y);

  printf("Valor de z:\n");
  scanf("%d", &z);

  printf("Valor de m:\n");
  scanf("%d", &m);

  if (x < y){

    m = x;

  } else {

    m = y;

  }

  if (m >= z){

    m = z;

  }

  printf("El minimo entre x, y, z es:\n min = %d\n", m);

  /*
x=2 ; y=4 ; z=1 ; m=8 => x=2 ; y=4 ; z=1 ; m=2 => x=2 ; y=4 ; z=8 ; m=1
*/

  // Este programa le da a "m" el valor del minimo entre x, y, z. Para el ejemplo el valor de m es 4.

  return 0;
}