#include <stdlib.h>
#include <stdio.h>

#include "strfuncs.h"

size_t string_length(const char *str){

    unsigned int i = 0 , length = 0;

    if (str == NULL){

        length = 0;

    } else {

        while (str[i] != '\0') {

            length ++;

            i ++;
            
        }
    }

    return length;
}

char *string_filter(const char *str, char c){

    unsigned int i = 0 , j = 0;

    char *pointer = NULL;
    pointer = malloc(sizeof(char) * string_length(str));

    while (str[i] != '\0') {

        if (str[i] != c) {

            pointer[j] = str[i];

            j ++;

        }

        i++;
    }

    pointer[j] = '\0';

    return pointer;
}