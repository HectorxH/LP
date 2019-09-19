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

    list l;
    init(&l);

    print(&l);
    append(&l, dato1);
    print(&l);
    insert(&l, 0, dato1);
    print(&l);
    insert(&l, 0, dato1);
    print(&l);

    clear(&l);

    printf("Nice\n");
    return 0;
}
