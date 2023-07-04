#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "stack.h"

struct _s_stack {

    stack_elem elem;
    stack next;
    unsigned int amount;
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
    p->amount = s == NULL? 1 : s->amount + 1;

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

    return s == NULL ? 0 : s->amount;
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

    for (unsigned int i = 0u; i < length ; i++) {

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