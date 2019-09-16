#include "funciones.h"

typedef struct list list;
typedef struct node node;
typedef struct dato data;

list* map(list* l, data (*f)(dato)){
    return l;
}
