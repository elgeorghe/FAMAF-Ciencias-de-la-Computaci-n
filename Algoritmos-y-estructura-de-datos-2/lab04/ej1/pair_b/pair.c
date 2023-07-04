#include <stdlib.h>  /* EXIT_SUCCESS... */
#include <stdio.h>   /* printf()...     */
#include "pair.h"    /* TAD Par         */

pair_t pair_new(int x, int y){
  
  pair_t par;
  par = malloc(sizeof(pair_t));
  par->fst = x;
  par->snd = y;


  return par;
}

int pair_first(pair_t p){

return p->fst;
}

int pair_second(pair_t p){

  return p->snd;
}

pair_t pair_swapped(pair_t p){

  int aux;
  aux = p->fst;
  p->fst = p->snd;
  p->snd = aux;

  return p;
}

pair_t pair_destroy(pair_t p){


  free(p);
  return NULL;
}