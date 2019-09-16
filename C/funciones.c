#include "funciones.h"

typedef struct list list;
typedef struct node node;
typedef struct dato data;

list* map(list* l, data (*f)(dato)){
    return l;
}

float sum(struct list* a){
  int i;
  float total = 0;
  int len = lenght(struct list* a);
  for (i=0; i<len; i++){
    total += at(a, i);
  }
  return total;
}
