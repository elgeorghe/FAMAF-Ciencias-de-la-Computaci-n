#include <assert.h>
#include <stdlib.h>

#include "dict.h"
#include "key_value.h"

struct _node_t {

    dict_t left;

    key_t key;
    value_t value;

    dict_t right;
};

static bool invrep(dict_t d) {

    bool inv = true;

    if (d == NULL || (d->left == NULL && d->right == NULL)){

        inv = true;
   
    } else if (d->right == NULL) {

        inv = inv && key_less(d->left->key , d->key) && invrep(d->left);

    } else if (d->left == NULL) {

        inv = inv && key_less(d->key , d->right->key) && invrep(d->right);

    } else {

        inv = inv && key_less(d->left->key , d->key) && key_less(d->key , d->right->key) && invrep(d->left) && invrep(d->right);

    }

    return inv;
}

dict_t dict_empty(void) {

    dict_t dict = NULL;

    assert(invrep(dict) && dict_length(dict) == 0);

    return dict;
}

dict_t dict_add(dict_t dict, key_t word, value_t def) {

    assert(invrep(dict));

    if (dict == NULL) {

        dict = malloc(sizeof(struct _node_t));

        dict->left = NULL;

        dict->key = word;
        dict->value = def;

        dict->right = NULL;

    } else if (key_eq(dict->key , word)) {

        dict->value = def;

    } else if (key_less(word , dict->key)) {

        dict->left = dict_add(dict->left , word, def);

    } else if (key_less(dict->key , word)) {

        dict->right = dict_add(dict->right , word, def);
    }

    assert(invrep(dict) && key_eq(def , dict_search(dict , word)));

    return dict;
}

value_t dict_search(dict_t dict, key_t word) {

    assert(invrep(dict));

    key_t def = NULL;

    if(dict != NULL) {

        if (key_eq(dict->key , word)) {

            def = dict->value;

        } else if (key_less(word , dict->key)) {

            def = dict_search(dict->left , word);

        } else if (key_less(dict->key , word)) {

            def = dict_search(dict->right , word);

        }
    }

    assert((def != NULL) == (dict_exists(dict , word)));

    return def;
}

bool dict_exists(dict_t dict, key_t word) {

    assert(invrep(dict));

    bool b = false;

    if (dict != NULL) {

        if (key_eq(dict->key , word)) {

            b = true;

        } else if (key_less(word , dict->key)) {


            b = dict_exists(dict->left , word);

        } else {

            b = dict_exists(dict->right , word);

        }
    }

    assert(invrep(dict));

    return b;
}

unsigned int dict_length(dict_t dict) {

    assert(invrep(dict));

    unsigned int length = 0u;

    if (dict != NULL) {

        length = 1 + dict_length(dict->left) + dict_length(dict->right);
    }

    return length;
}

static dict_t minNode(dict_t dict){

    dict_t min = dict ;

    while (min != NULL && min->left !=NULL) {

        min = min->left;
    }

    return min;
}

dict_t dict_remove(dict_t dict, key_t word) {

    assert(invrep(dict));

    if (dict_exists(dict,word) || dict != NULL) {

        if (key_eq(dict->key,word)) {

            if (dict->left == NULL) {

                dict_t temp = dict;

                dict = dict->right;

                temp->key = key_destroy(temp->key);
                temp->value = value_destroy(temp->value);

                free(temp);

            } else if (dict->right == NULL) {

                dict_t temp = dict;

                dict = dict->left;

                temp->key = key_destroy(temp->key);
                temp->value = value_destroy(temp->value);

                free(temp);

            } else {
                
                dict_t temp = minNode(dict->right);

                dict->key = temp->key;
                dict->value = temp->value;

                dict->right = dict_remove(dict->right , temp->key);
            }

        } else if (key_less(dict->key,word)) {

            dict->right = dict_remove(dict->right,word);

        } else {

            dict->left = dict_remove(dict->left,word);
        } 
        
    }

    assert(invrep(dict) && !dict_exists(dict, word));

    return dict;
}

dict_t dict_remove_all(dict_t dict) {

    assert(invrep(dict));

    if (dict != NULL){

        dict->key = key_destroy(dict->key);
        dict->value = value_destroy(dict->value);

        dict->left = dict_remove_all(dict->left);
        dict->right = dict_remove_all(dict->right);

        free (dict);

        dict = NULL;
    }
    assert(invrep(dict) && dict_length(dict) == 0);
    
    return dict;
}

void dict_dump(dict_t dict, FILE *file) {

    assert(invrep(dict) && file != NULL);

    if(dict != NULL) {

        dict_dump(dict->left,file);
        key_dump(dict->key,file);
        fprintf(file," : ");
        value_dump(dict->value,file);
        fprintf(file,"\n");
        dict_dump(dict->right,file);
    }
}

dict_t dict_destroy(dict_t dict) {

    assert(invrep(dict));

    if (dict != NULL) {

        dict_remove_all(dict);

        dict = NULL;
    }

    assert(dict == NULL);

    return dict;
}
