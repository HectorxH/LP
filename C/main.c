#include <stdio.h>
#include <stdlib.h>
#include "lista.h"
#include "funciones.h"

typedef struct list list;

int main(){
    dato dato1;
    int a = 20;
    dato1.tipo = 'i';
    dato1.contenido = &a;

    dato dato2;
    float b = 30.5;
    dato2.tipo = 'f';
    dato2.contenido = &b;

    dato dato3;
    dato3.tipo = 'l';
    list ld3;
    init(&ld3);
    append(&ld3, dato1);
    insert(&ld3, 1, dato2);
    append(&ld3, dato2);
    print(&ld3);
    dato3.contenido = &ld3;

    list l;
    init(&l);
    print(&l);
    append(&l, dato1);
    print(&l);
    insert(&l, 0, dato2);
    print(&l);
    insert(&l, 0, dato1);
    print(&l);
    insert(&l, 0, dato3);
    append(&l, dato3);
    print(&l);

    float suma = sum(&l);
    printf("%f\n", suma);

    float prom = average(&l);
    printf("%f\n", prom);

    clear(&l);
    return 0;
}
