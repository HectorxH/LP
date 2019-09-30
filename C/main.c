#include <stdio.h>
#include <stdlib.h>
#include "lista.h"
#include "funciones.h"

typedef struct list list;

int main(){
    dato dato1;
    int a = 1;
    dato1.tipo = 'i';
    dato1.contenido = &a;

    dato dato2;
    int b = 2;
    dato2.tipo = 'i';
    dato2.contenido = &b;

    dato dato3;
    float c = 3.0;
    dato3.tipo = 'f';
    dato3.contenido = &c;

    dato dato4;
    dato4.tipo = 'l';
    list ld4;
    init(&ld4);
    dato4.contenido = &ld4;

    dato dato5;
    dato5.tipo = 'l';
    list ld5;
    init(&ld5);
    dato5.contenido = &ld5;
    append(&ld5, dato1);
    append(&ld5, dato2);
    append(&ld5, dato3);

    dato dato6;
    dato6.tipo = 'l';
    list ld6;
    init(&ld6);
    dato6.contenido = &ld6;
    append(&ld6, dato3);
    append(&ld6, dato1);
    append(&ld6, dato2);

    dato dato7;
    dato7.tipo = 'l';
    list ld7;
    init(&ld7);
    dato7.contenido = &ld7;
    append(&ld7, dato5);
    append(&ld7, dato6);

    list l;
    init(&l);
    insert(&l, 0, dato4);
    append(&l, dato1);
    append(&l, dato2);
    insert(&l, 3, dato3);
    append(&l, dato7);
    print(&l);
    remov(&l, 1);
    remov(&l, 1);
    remov(&l, 2);
    print(&l);

    float suma = sum(&l);
    printf("Suma = %f\n", suma);
    float prom = average(&l);
    printf("Promedio = %f\n", prom);

    clear(&l);
    clear(&ld4);
    clear(&ld5);
    clear(&ld6);
    clear(&ld7);
    return 0;
}
