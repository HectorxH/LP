#include "funciones.h"
#include "lista.h"
#include <stdio.h>
#include <stdlib.h>

typedef struct list list;
typedef struct node node;
typedef struct dato dato;

list* map(list* a, dato (*f)(dato)){
    int i;
    int len = length(a);
    list* l = (list*)malloc(sizeof(list));
    init(l);
    for (i=0; i<len; i++){
        dato d = *at(a, i);
        char tipo_d = getTipo(&d);
        if(tipo_d == 'l')
            setContenido(&d, map((list*)getContenido(&d), f));
        else if(tipo_d == 'i' || tipo_d == 'f')
            d = f(d);
        append(l, d);
        clear((list*)getContenido(&d));
        free(getContenido(&d));
    }
    return l;
}

float sum(list* a){
    int i;
    float total = 0;
    int len = length(a);
    for (i=0; i<len; i++){
        dato* d = at(a, i);
        char tipo_d = getTipo(d);
        if(tipo_d == 'l')
            total += sum((list*)getContenido(d));
            else if(tipo_d == 'i')
            total += *(int*)getContenido(d);
        else if(tipo_d == 'f')
            total += *(float*)getContenido(d);
    }
    return total;
}

/*
print_aux
Función que muestra en pantalla la lista y sus contenidos de forma recursiva.
No termina con salto de linea.
——————————————–
Inputs:
(list*) Lista que se mostrará en pantalla.
——————————————–
Output:
(void) No retorna.
*/

void print_aux(list* a){
    int i;
    int len = length(a);
    printf("[");
    for(i=0; i<len; i++){
        dato* d = at(a, i);
        char tipo_d = getTipo(d);
        if(tipo_d == 'l')
            print_aux((list*)getContenido(d));
        else if(tipo_d == 'i')
            printf("%d", *(int*)getContenido(d));
        else if(tipo_d == 'f')
            printf("%f", *(float*)getContenido(d));
        if (i != len-1)
            printf(", ");
    }
    printf("]");
    return;
}

void print(list* a){
    print_aux(a);
    printf("\n");
    return;
}

float average(list* a){
    int i, n, len;
    n = len =length(a);
    float suma = 0;
    for (i=0; i<len; i++){
        dato* d = at(a, i);
        char tipo_d = getTipo(d);
        if(tipo_d == 'l')
            if(length((list*)getContenido(d)) == 0) n--;
            else suma += average((list*)getContenido(d));
        else if(tipo_d == 'i')
            suma += *(int*)getContenido(d);
        else if(tipo_d == 'f')
            suma += *(float*)getContenido(d);
    }
    if (n == 0){
      printf("Error: El promedio no está definido para esta lista.\n");
      return 0;
    }
    return suma/n;
}
