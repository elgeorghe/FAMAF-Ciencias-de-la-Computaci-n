/*
  @file sort.c
  @brief sort functions implementation
*/

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include "helpers.h"
#include "sort.h"
#include "player.h"

bool goes_before(player_t x, player_t y){

    bool res;

    // Veo si el ranking de 'x' es menor o igual al de 'y'
    // Como ahora estoy trabajando con punteros, tengo que acceder al valor guardado en el. 
    
    res = x->rank <= y->rank;        

    return res;
}

bool array_is_sorted(player_t atp[], unsigned int length) {
    unsigned int i = 1u;
    while (i < length && goes_before(atp[i - 1u], atp[i])) {
        i++;
    }
    return (i == length);
}

/*
    Voy utilizar el selection sort. Copio el codigo del lab02 ej4
*/

static void swap(player_t a[], unsigned int izq, unsigned int der) {

    // aux ahora es un puntero

    player_t aux;

    aux = a[izq];
    a[izq] = a[der];
    a[der] = aux;

}

static unsigned int min_pos_from(player_t a[], unsigned int i, unsigned int length) {
    unsigned int min_pos = i;
    for (unsigned int j = i + 1; j < length; ++j) {
        if (!goes_before(a[min_pos],a[j])) {
            min_pos = j;
        }
    }
    return (min_pos);
}

void sort(player_t a[], unsigned int length) {

    for (unsigned int i = 0u; i < length; ++i) {

        unsigned int min_pos = min_pos_from(a, i, length);
        swap(a, i, min_pos);
    }
}