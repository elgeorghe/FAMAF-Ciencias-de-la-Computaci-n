#include <stdio.h>
#include <stdlib.h>
#include "string.h"

int main (void) {

    char *palabra1 = "Avenida";
    char *palabra2 = "Avellanda";

    string str1 = string_create(palabra1);
    string str2 = string_create(palabra2);

    printf("\n La palabra 1 es: ");
    string_dump(str1, stdout);

    printf("\n La palabra 2 es: ");
    string_dump(str2, stdout);

    printf("\n palabra 1 <= palabra 2 : %s\n", string_less(str1, str2) ? "True" : "False");

    printf("palabra 1 == palabra 2 : %s\n", string_eq(str1, str2) ? "True" : "False");

    str1 = string_destroy(str1);
    str2 = string_destroy(str2);

    return EXIT_SUCCESS;
}
