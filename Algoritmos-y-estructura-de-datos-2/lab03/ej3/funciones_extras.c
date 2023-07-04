#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

// Incluyo la libreria de funcions extras
#include "funciones_extras.h"


char *parse_filepath (int argc , char *argv[]) {

    /* Parse the filepath given by command line argument. */
    char *result = NULL;
    // Program takes exactly two arguments
    // (the program's name itself and the input-filepath)
    bool valid_args_count = (argc == 2);

    if (!valid_args_count) {        
        exit(EXIT_FAILURE);
    }

    result = argv[1];
    return result;
}


unsigned int data_from_file(const char *path, unsigned int indexes[], char letters[], unsigned int max_size) {

    unsigned int i = 0u; 

    // Creo un puntero de archivo
    FILE *archivo = NULL;

    // Abro el archivo que se encuentra en path en modo lectura
    archivo = fopen(path , "r");
    
    // Chequeo de que se haya podio leer el archivo
    if (archivo == NULL) {

        fprintf(stderr, "File does not exist.\n");
        exit(EXIT_FAILURE);

    }
    
    // Mientras que no llegue al final del archivo sigo leyendo los datos
    while (!feof(archivo)) {

        /*
            Como el formato es <int> -> *<char>* , utilizo ese formato de fscanf
            A medida que voy leyendo los datos, los voy guardando en su array correspondiente
        */
        fscanf(archivo, "%u -> *%c*\n" , &indexes[i] , &letters[i]);

        /*
            Luego de leer, chequeo que ningun indice supere el max_size
            Es otra forma de saber si el largo de la frase entra en max_size        
        */

        if (indexes[i] > max_size) {

            fprintf(stderr, "Allowed size is %d.\n", max_size);
            exit(EXIT_FAILURE);

        }
        
        i++;
    }    

    // Cierro el archivo
    fclose(archivo);

    // Devuelvo la cantidad de elementos que hay en el archivo
    return i;
}


void sort(char sorted[] , unsigned int indexes[] , char letters[] , unsigned int length){

    // Para resolver esto utilizo punteros
    unsigned int *direc_indice = NULL;
    char *direc_sorted = NULL;

    // Voy colocando cada letra donde va
    for (size_t i = 0; i < length; i++) {

        /* 
            Primero, tomo la direccion donde esta guardado el valor del indice de la letra a colocar
        */
        direc_indice = &indexes[i];

        /* 
            Segundo, encuentro donde va mi letra en el arreglo ordenado usando el valor del indice
            que estaba en la direccion anterior
        */
        direc_sorted = &sorted[*direc_indice];

        /* 
            Tercero, modifico ese lugar con la letra que va
        */
        *direc_sorted = letters[i];
        
    }
}



