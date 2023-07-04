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

// Estructura de div_t
typedef struct {

  int cociente;
  int resto;

} div_t;

// Funcion que devuelve una estructura div_t
div_t division(int x, int y){

  div_t nuevatupla;
  nuevatupla.cociente = x/y;
  nuevatupla.resto = x%y;
  return nuevatupla;

}

int main(void){

  int x,y,c,r;

  printf("Valor de x:\n");
  scanf("%d", &x);

  printf("Valor de y:\n");
  scanf("%d", &y);

  if (y == 0) {

    printf("Error, divisor Nulo\n");

  } else {

    div_t tupla = division(x,y);
    c = tupla.cociente;
    r = tupla.resto;

    printf("El cociente y el resto son:\n c=%d ; r=%d\n" , c,r);   

  }

  return 0;
}