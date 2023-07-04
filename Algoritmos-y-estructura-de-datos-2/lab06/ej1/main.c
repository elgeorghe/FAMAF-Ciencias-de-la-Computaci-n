/* First, the standard lib includes, alphabetically ordered */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "abb.h" /* TAD abb */


void print_help(char *program_name) {
    /* Print the usage help of this program. */
    printf("Usage: %s <input file path>\n\n",
           program_name);
}

char *parse_filepath(int argc, char *argv[]) {
    /* Parse the filepath given by command line argument. */
    char *result = NULL;

    if (argc < 2) {
        print_help(argv[0]);
        exit(EXIT_FAILURE);
    }

    result = argv[1];

    return (result);
}

abb abb_from_file(const char *filepath) {
    FILE *file = NULL;
    abb read_tree;

    read_tree = abb_empty();
    file = fopen(filepath, "r");
    if (file == NULL) {
        fprintf(stderr, "File does not exist.\n");
        exit(EXIT_FAILURE);
    }
    unsigned int i = 0u;
    unsigned int size = 0u;
    int res = 0;
    res = fscanf(file, " %u ", &size);
    if (res != 1) {
        fprintf(stderr, "Invalid format.\n");
        exit(EXIT_FAILURE);
    }
    while (i < size) {
        abb_elem elem;
        res = fscanf(file," %d ", &(elem));
        if (res != 1) {
            fprintf(stderr, "Invalid array.\n");
            exit(EXIT_FAILURE);
        }
        read_tree = abb_add(read_tree, elem);

       ++i;
    }
    fclose(file);
    return read_tree;
}

int main(int argc, char *argv[]) {

    char *filepath = NULL;

    /* parse the filepath given in command line arguments */
    filepath = parse_filepath(argc, argv);

    /* parse the file to obtain an abb with the elements */
    abb tree = abb_from_file(filepath);

    /*
     * Modificar e implementar con un ciclo una interfaz que permita al usuario
     * realizar una de las siguientes operaciones en cada iteración:
     *
     * 1 ........ Mostrar árbol por pantalla
     * 2 ........ Agregar un elemento
     * 3 ........ Eliminar un elemento
     * 4 ........ Chequear existencia de elemento
     * 5 ........ Mostrar longitud del árbol
     * 6 ........ Mostrar raiz, máximo y mínimo del árbol
     * 7 ........ Salir
     *
     * Se debe solicitar un número de entrada para realizar una de las acciones.
     *
     * Para las opciones 2, 3 y 4 se le deberá pedir al usuario que ingrese el
     * elemento a agregar, eliminar o chequear respectivamente.
     *
     * Al salir debe liberarse toda la memoria utilizada.
     *
    */

    unsigned int option = 0u;
    int input;

    while (option != 7) {

        printf("\n Choose what you want to do. Options are:\n"
           "\n"
           "\t---------------------------------------------------------------\n"
           "\t* 1: Mostrar árbol por pantalla                               |\n"
           "\t* 2: Agregar un elemento                                      |\n"
           "\t* 3: Eliminar un elemento                                     |\n"
           "\t* 4: Chequear existencia de elemento                          |\n"
           "\t* 5: Mostrar longitud del árbol                               |\n"
           "\t* 6: Mostrar raiz, máximo y mínimo del árbol                  |\n"
           "\t* 7: Salir                                                    |\n"
           "\t---------------------------------------------------------------\n"
           "\n Please enter your choice: ");

        scanf(" %u", &option);
        if (option != 1 && option != 2 && option != 3 && option != 4 &&
            option != 5 && option != 6 && option != 7) {

            printf("Ingresar una opción q sea válida \n\n");
        }

        switch(option) {
            case 1:
                abb_dump(tree);
                break;

            case 2:
                printf("Ingresar elemento que desea agregar: ");
                scanf("%d", &input);
                abb_add(tree, input);
                break;

            case 3:
                printf("Ingresar elemento que desea eliminar: ");
                scanf("%d", &input);
                abb_remove(tree, input);
                break;

            case 4:
                printf("Ingresar elemento que desea verificar que existe: ");
                scanf("%d", &input);
                printf("%s", abb_exists(tree, input) ? "Si existe el elemento \n" : "No existe el elemento \n");
                break;

            case 5:
                printf("La longitud del árbol es: %u \n", abb_length(tree));
                break;

            case 6:
                if (!abb_is_empty(tree)) {

                    printf("\n");
                    printf("raiz: %d\n minimo: %d\n maximo: %d\n", abb_root(tree), abb_min(tree), abb_max(tree));

                } else {

                    printf("\nÁrbol vacío\n");
                }

                break;

            default:
                break;
        }
    };

    tree = abb_destroy(tree);

    return (EXIT_SUCCESS);
}

/*
    El abb_dump() original muestra los elementos en orden porque va hasta el elemento mas a la izq (por ende el mas chico) y printea de izq a der.
    El arbol que se formaria en caso de agregar todos los elementos en ese orden seria un arbol solo con ramas derechas.
*/
