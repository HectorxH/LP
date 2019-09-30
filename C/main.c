#include <stdio.h>
#include <stdlib.h>
#include "lista.h"
#include "funciones.h"

dato funcioncita(dato datito){
    if(datito.tipo == 'i'){
        int* temp = (int*)malloc(sizeof(int));
        *temp = *(int*)datito.contenido + 69;
        datito.contenido = temp;
    }
    else if(datito.tipo == 'f'){
        float* temp = (float*)malloc(sizeof(float));
        *temp = *(float*)datito.contenido + 69;
        datito.contenido = temp;
    }
    return datito;
}

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
    insert(&ld7, 0, dato6);

    list l;
    init(&l);
    insert(&l, 0, dato4);
    append(&l, dato1);
    append(&l, dato2);
    insert(&l, 3, dato3);
    append(&l, dato7);
    print(&l);

    float suma1 = sum(&l);
    printf("Suma = %f\n", suma1);
    float prom1 = average(&l);
    printf("Promedio = %f\n", prom1);

    remov(&l, 1);
    remov(&l, 1);
    print(&l);

    float suma2 = sum(&l);
    printf("Suma = %f\n", suma2);
    float prom2 = average(&l);
    printf("Promedio = %f\n", prom2);

    list* map_list = map(&l, funcioncita);
    print(map_list);

    clear(map_list);
    free((void*)map_list);

    clear(&l);
    clear(&ld4);
    clear(&ld5);
    clear(&ld6);
    clear(&ld7);
    return 0;
}
