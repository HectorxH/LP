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

    list l;
    init(&l);
    insert(&l, 0, dato4);
    append(&l, dato5);
    insert(&l, 1, dato1);
    append(&l, dato3);
    insert(&l, 2, dato2);
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
    return 0;
}
