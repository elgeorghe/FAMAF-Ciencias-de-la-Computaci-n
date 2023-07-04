#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "stack.h"

struct _s_stack {

    stack_elem elem;
    stack next;
};

stack stack_empty(){

    stack s = NULL;

    return s;
}

stack stack_push(stack s, stack_elem e){

    struct _s_stack *p = NULL;
    p = malloc(sizeof(struct _s_stack));
    
    p->elem = e;
    p->next = s;

    s = p;

    return s;
}

stack stack_pop(stack s){

    assert(!stack_is_empty(s));

    struct _s_stack *p = NULL;

    p = s;

    s = s->next;

    free(p);

    return s;
}

unsigned int stack_size(stack s){

    struct _s_stack *p = NULL;

    unsigned int n = 0u;

    p = s;

    while (p != NULL) {
        
        n ++;
        p = p->next;
    }

    return n;
}

stack_elem stack_top(stack s){

    assert(!stack_is_empty(s));

    stack_elem e;

    e = s->elem;

    return e;
}

bool stack_is_empty(stack s){

    bool b;

    b = (s == NULL);

    return b;
}

stack_elem *stack_to_array(stack s){

    stack point = s;

    stack_elem *a = NULL;
    a = calloc(stack_size(s) , sizeof(stack_elem));

    unsigned int length = stack_size(s);

    for (int i = length - 1; i >= 0 ; i--) {

        a[i] = point->elem;

        point = point->next;
    }
    
    return a;
}

stack stack_destroy(stack s){

    struct _s_stack *p = NULL;
    
    p = s;
    
    if (p != NULL) {

        while (p->next != NULL) {

            s = stack_pop(s);

            p = s;
        }
        
        free(p);

        p =  NULL;
        s = NULL;
    }

    return s;
}