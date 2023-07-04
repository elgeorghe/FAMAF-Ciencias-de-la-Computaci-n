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

// Estructura de persona_t
typedef struct _persona{

  char *nombre;
  int edad;
  float altura;
  float peso;

} persona_t;

float peso_promedio(persona_t arr[], unsigned int longitud){

  unsigned int i = 0 ;
  float sum = 0 , prom;

  while (i < longitud) {

    sum += arr[i].peso;

    i ++;    
  }

  prom = sum / longitud;

  return prom;
}


persona_t persona_de_mayor_edad(persona_t arr[], unsigned int longitud){

  unsigned int i = 0 ;

  persona_t persona_mayor;

  persona_mayor.nombre = 0;
  persona_mayor.edad = INT_MIN;
  persona_mayor.altura = 0;
  persona_mayor.peso = 0;  

  while (i < longitud){

    if (arr[i].edad > persona_mayor.edad){

      persona_mayor.nombre = arr[i].nombre;
      persona_mayor.edad = arr[i].edad;
      persona_mayor.altura = arr[i].altura;
      persona_mayor.peso = arr[i].peso;
    }

    i ++;

  }

  return persona_mayor;

}

persona_t persona_de_menor_altura(persona_t arr[], unsigned int longitud){

  unsigned int i = 0;

  persona_t persona_menor;

  persona_menor.nombre = 0;
  persona_menor.edad = 0;
  persona_menor.altura = INT_MAX;
  persona_menor.peso = 0;

  while (i < longitud){

    if (arr[i].altura < persona_menor.altura){

      persona_menor.nombre = arr[i].nombre;
      persona_menor.edad = arr[i].edad;
      persona_menor.altura = arr[i].altura;
      persona_menor.peso = arr[i].peso;
    }

    i++;
  }

  return persona_menor;
}

int main(void){

  persona_t p1 = {"Paola", 21, 1.85, 75};
  persona_t p2 = {"Luis", 54, 1.75, 69};
  persona_t p3 = {"Julio", 40, 1.70, 80};

  unsigned int longitud = 3;

  persona_t arr[] = {p1, p2, p3};

  printf("El peso promedio es %f\n", peso_promedio(arr, longitud));

  persona_t p = persona_de_mayor_edad(arr, longitud);

  printf("El nombre de la persona con mayor edad es %s\n", p.nombre);

  p = persona_de_menor_altura(arr, longitud);

  printf("El nombre de la persona con menor altura es %s\n", p.nombre);

  return 0;
}
