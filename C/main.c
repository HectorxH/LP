#include <stdio.h>
#include <stdlib.h>
#include "lista.h"
#include "funciones.h"

typedef struct list list;

int main(){
    dato dato1;
    dato1.tipo = 'i';
    dato1.contenido = (void*)malloc(sizeof(int));
    *((int*)dato1.contenido) = 20;

    list l;
    init(&l);
    append(&l, dato1);
    print(&l);
    clear(&l);

    printf("Nice");
    return 0;
}
