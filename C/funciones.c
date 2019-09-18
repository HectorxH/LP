#include "funciones.h"
#include "lista.h"
#include <stdio.h>

typedef struct list list;
typedef struct node node;
typedef struct dato dato;

list* map(list* a, dato (*f)(dato)){
    int i;
    int len = length(a);
    for (i=0; i<len; i++){
        dato* d = at(a, i);
        char tipo_d = d->tipo;
        if(tipo_d == 'l')
            d->contenido = map((list*)d->contenido, f);
        else if(tipo_d == 'i' || tipo_d == 'f')
            *d = f(*d);
    }
    return a;
}

float sum(list* a){
    int i;
    float total = 0;
    int len = length(a);
    for (i=0; i<len; i++){
        dato* d = at(a, i);
        char tipo_d = d->tipo;
        if(tipo_d == 'l')
            total += sum((list*)d->contenido);
            else if(tipo_d == 'i')
            total += *((int*)d->contenido);
        else if(tipo_d == 'f')
            total += *((float*)d->contenido);
    }
    return total;
}

void print_aux(list* a){
    int i;
    int len = length(a);
    printf("[");
    for(i=0; i<len; i++){
        dato* d = at(a, i);
        char tipo_d = d->tipo;
        if(tipo_d == 'l')
            print((list*)d->contenido);
        else if(tipo_d == 'i')
            printf("%d", *((int*)d->contenido));
        else if(tipo_d == 'f')
            printf("%f", *((float*)d->contenido));
        if (i != len-1)
            printf(", ");
    }
    printf("]");
    return;
}

void print(struct list* a){
    int i;
    int len = length(a);
    printf("[");
    for(i=0; i<len; i++){
        dato* d = at(a, i);
        char tipo_d = d->tipo;
        if(tipo_d == 'l')
            print_aux((list*)d->contenido);
        else if(tipo_d == 'i')
            printf("%d", *((int*)d->contenido));
        else if(tipo_d == 'f')
            printf("%f", *((float*)d->contenido));
        if (i != len-1)
            printf(", ");
    }
    printf("]\n");
    return;
}

float average(struct list* a){
    int i, n, len;
    n = len =length(a);
    float suma = 0;
    for (i=0; i<len; i++){
        dato* d = at(a, i);
        char tipo_d = d->tipo;
        if(tipo_d == 'l')
            if(length((list*)d->contenido) == 0) n--;
            else suma += average((list*)d->contenido);
        else if(tipo_d == 'i')
            suma += *((int*)d->contenido);
        else if(tipo_d == 'f')
            suma += *((float*)d->contenido);
    }
    return suma/len;
}
