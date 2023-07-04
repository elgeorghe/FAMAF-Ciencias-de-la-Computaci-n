#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <assert.h>
#include "abb.h"

struct _s_abb {

    abb_elem elem;
    struct _s_abb *left;
    struct _s_abb *right;

};

static bool elem_eq(abb_elem a, abb_elem b) {

    return a == b;
}

static bool elem_less(abb_elem a, abb_elem b) {

    return a < b;
}

static bool invrep(abb tree) {
    
    bool inv = true;

    if (tree == NULL || (tree->left == NULL && tree->right == NULL)){

        inv = true;
   
    } else if (tree->right == NULL) {

        inv = inv && elem_less(tree->left->elem , tree->elem) && invrep(tree->left);

    } else if (tree->left == NULL) {

        inv = inv && elem_less(tree->elem , tree->right->elem) && invrep(tree->right);

    } else {

        inv = inv && elem_less(tree->left->elem , tree->elem) && elem_less(tree->elem , tree->right->elem) && invrep(tree->left) && invrep(tree->right);

    }

    return true;
}

abb abb_empty(void) {

    abb tree;
    
    tree = NULL;

    assert(invrep(tree) && abb_is_empty(tree));

    return tree;
}

abb abb_add(abb tree, abb_elem e) {

    assert(invrep(tree));

    if (tree == NULL){

        tree = malloc(sizeof(struct _s_abb));

        tree->elem = e;
        tree->left = NULL;
        tree->right = NULL;

    } else if (elem_less(e,tree->elem)){

        tree->left = abb_add(tree->left, e);

    } else if (elem_less(tree->elem , e)) {

        tree->right = abb_add(tree->right , e);
    }

    assert(invrep(tree) && abb_exists(tree , e));

    return tree;
}

bool abb_is_empty(abb tree) {

    assert(invrep(tree));

    return tree == NULL;
}

bool abb_exists(abb tree, abb_elem e) {

    bool exists = false;

    assert(invrep(tree));

    if (abb_is_empty(tree)) {

        exists = false;

    } else if (elem_eq(tree->elem , e)) {

        exists = true;

    } else if (elem_less(tree->elem , e)) {

        exists = abb_exists(tree->right , e);

    } else {

        exists = abb_exists(tree->left , e);
    }

    return exists;
}

unsigned int abb_length(abb tree) {

    unsigned int length = 0;

    assert(invrep(tree));

    if (!abb_is_empty(tree)) {

        length = 1 + abb_length(tree->left) + abb_length(tree->right);

    }

    assert(invrep(tree) && (abb_is_empty(tree) || length > 0));

    return length;
}

abb abb_remove(abb tree, abb_elem e) {

    assert(invrep(tree));

    if (tree != NULL) {

        if (elem_less(e,tree->elem)) {

            tree->left = abb_remove(tree->left , e);

        } else if (elem_less(tree->elem , e)) {

            tree->right = abb_remove(tree->right , e);

        } else {

            abb temp = NULL;

            if (tree->left == NULL) {

                temp = tree;
                tree = tree->right;
                free(temp);

            } else if (tree->right == NULL) {

                temp = tree;
                tree = tree->left;
                free(temp);

            } else {

                temp = tree->right;

                while(temp && temp->left != NULL){

                    temp = temp->left;
                }

                tree->elem = temp->elem;
                tree->right = abb_remove(tree->right,temp->elem);
            }
        }
    }

    assert(invrep(tree) && !abb_exists(tree, e));

    return tree;
}


abb_elem abb_root(abb tree) {

    abb_elem root;

    assert(invrep(tree) && !abb_is_empty(tree));
   
    root = tree->elem;

    assert(abb_exists(tree, root));
    
    return root;
}

abb_elem abb_max(abb tree) {

    abb_elem max_e;

    assert(invrep(tree) && !abb_is_empty(tree));
    
    if (abb_is_empty(tree->right)) {

        max_e = abb_root(tree);
        
    } else {

        max_e = abb_max(tree->right);

    }

    assert(invrep(tree) && abb_exists(tree, max_e));
    return max_e;
}

abb_elem abb_min(abb tree) {

    abb_elem min_e;

    assert(invrep(tree) && !abb_is_empty(tree));

    if (abb_is_empty(tree->left)) {

        min_e = abb_root(tree);
        
    } else {

        min_e = abb_min(tree->left);

    }

    assert(invrep(tree) && abb_exists(tree, min_e));

    return min_e;
}

void abb_dump(abb tree) {

    assert(invrep(tree));

    if (tree != NULL) {

        printf("%d ", tree->elem);
        abb_dump(tree->left);
        abb_dump(tree->right);
    }
}

abb abb_destroy(abb tree) {

    assert(invrep(tree));

    if (!abb_is_empty(tree)) {

        tree->left = abb_destroy(tree->left);
        tree->right = abb_destroy(tree->right);
        free(tree);
        tree = NULL;
    }

    assert(tree == NULL);

    return tree;
}
