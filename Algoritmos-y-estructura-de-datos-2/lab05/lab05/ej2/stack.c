#include <stdlib.h>
#include <assert.h>
#include "stack.h"

struct _s_stack {
    stack_elem *elems;      // Arreglo de elementos
    unsigned int size;      // Cantidad de elementos en la pila
    unsigned int capacity;  // Capacidad actual del arreglo elems
};

stack stack_empty(){

    stack s = malloc(sizeof(struct _s_stack));

    s->elems = NULL;
    s->size = 0u;
    s->capacity = 0u;

    return s;
}

stack stack_push(stack s, stack_elem e){

    if (stack_is_empty(s)){

        s->capacity = 1u;

        s->elems = calloc(s->capacity , sizeof(stack_elem));

    } else if (s->size >= s->capacity){

        s->capacity = 2 * s->capacity;

        s->elems = realloc(s->elems , (s->capacity) * sizeof(stack_elem) );
        
    }

    s->elems[s->size] = e;

    s->size ++;

    return s;
}

stack stack_pop(stack s){

    assert(!stack_is_empty(s));

    s->size --;

    return s;
}

unsigned int stack_size(stack s){

    return s->size;
}

stack_elem stack_top(stack s){

    assert(!stack_is_empty(s));

    return s->elems[s->size - 1u];
}

bool stack_is_empty(stack s){

    return (s->size == 0u) ;
}

stack_elem *stack_to_array(stack s){

    stack_elem *a = NULL;
    a = calloc(stack_size(s) , sizeof(stack_elem));

    unsigned int length = stack_size(s);

    for (unsigned int i = 0u; i < length ; i++) {

        a[i] = s->elems[i];
    }
    
    return a;
}

stack stack_destroy(stack s){

    free(s->elems);
    s->elems = NULL;
    free(s);
    s = NULL;

    return s;
}
