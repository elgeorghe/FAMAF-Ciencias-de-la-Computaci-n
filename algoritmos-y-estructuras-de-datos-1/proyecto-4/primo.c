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

bool es_primo(int N){

  int i = 2 ;

  while (N % i != 0){

    i ++;

  }

  return ( i == N);

}

int nesimo_primo(int N){

  int i = 2 , contador = 1 , n_primo = 0;
  bool temp = true;
  
  while (temp){

    if (es_primo(i)) {

      if (contador == N){

        n_primo = i;
        temp = false;

      } else {

        contador ++;

      }
    }

    i ++;
  }

  return n_primo;    
}

int main(void){

  int x , primo;

  printf("Ingeres un numero positivo:\n");
  scanf("%d" , &x);

  if (x <= 0){

    printf("Error, numero no positivo\n");

  } else {

    primo = nesimo_primo(x);

    printf("El n-esimo primo es: %d\n", primo);

  }
  
  return 0;
}
