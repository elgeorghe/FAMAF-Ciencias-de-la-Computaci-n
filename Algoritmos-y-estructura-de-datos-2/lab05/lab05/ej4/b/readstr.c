#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LENGTH 20

int main(void) {

    char user_input[MAX_LENGTH];

    printf("Ingrese su nombre y apellido: ");

    /*
        El scanf() no leia el apellido por el espacio.
        fgets lee todo pero agrega un \n al final.
    */

    fgets(user_input , MAX_LENGTH , stdin );

    // Reemplazo el \n por el \0 de fin de palabra
    user_input[strlen(user_input) - 1] = '\0';
    
    printf("Te damos la bienvenida %s a este maravilloso programa!\n", user_input);

    return EXIT_SUCCESS;
}



