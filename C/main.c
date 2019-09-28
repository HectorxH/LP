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
    dato1.tipo = 'i';
    dato1.contenido = &b;

    dato dato3;
    float c = 3.0;
    dato2.tipo = 'f';
    dato2.contenido = &c;

    /*dato dato4;
    dato4.tipo = 'l';
    list ld4;
    init(&ld4);
    dato3.contenido = &ld4;*/

    list l;
    init(&l);
    append(&l, dato2);
    insert(&l, 0, dato1);
    append(&l, dato3);
    print(&l);

    float suma = sum(&l);
    printf("Suma = %f\n", suma);
    float prom = average(&l);
    printf("Promedio = %f\n", prom);

    clear(&l);
    //clear(&ld4);
    return 0;
}
