#include <stdlib.h>
#include <stdio.h>
#include "lista.h"

typedef struct list list;
typedef struct node node;
typedef struct dato dato;

/*
free_node
Libera la memoria de un nodo y su contenido.
——————————————–
Inputs:
(node*) Nodo al que se le liberará la memoria.
——————————————–
Output:
(void) No retorna.
*/

void free_node(node* n){
    if(n->info.tipo == 'l') clear((list*)n->info.contenido);
    free((void*)n->info.contenido);
    free((void*)n);
}

/*
copy_dato
Copia el dato entregado y lo retorna.
——————————————–
Inputs:
(dato) Dato que se quiere copiar.
——————————————–
Output:
(dato) Retorna el dato entregado.
*/
dato copy_dato(dato d){
    void* contenido = d.contenido;
    char tipo = d.tipo;
    void* ptr;
    if(tipo == 'i'){
        ptr = malloc(sizeof(int));
        *(int*)ptr = *(int*)contenido;
    }
    else if(tipo == 'f'){
        ptr = malloc(sizeof(float));
        *(float*)ptr = *(float*)contenido;
    }
    else if(tipo == 'l'){
        list* l = (list*)contenido;
        ptr = malloc(sizeof(list));
        init((list*)ptr);
        for(int i = 0; i < l->length; i++){
            append((list*)ptr, *at(l, i));
        }
    }

    return (dato) {.contenido = ptr, .tipo = tipo};
}

/*
getTipo
Obtiene el tipo del dato entregado.
——————————————–
Inputs:
(dato*) Dato que se quiere obtener su tipo.
——————————————–
Output:
(char) Retorna el tipo del dato entregado.
*/
char getTipo(dato* d){
    return d->tipo;
}

/*
setTipo
Recibe un dato y un tipo, y le asigna este tipo al dato.
——————————————–
Inputs:
(dato*) Dato al que se le asignará el tipo.
(char) Tipo que se asignará al dato.
——————————————–
Output:
(void) No retorna.
*/
void setTipo(dato* d, char t){
    d->tipo = t;
}

/*
getContenido
Obtiene el contenido del dato entregado a la función.
——————————————–
Inputs:
(dato*) Dato que se quiere obtener su contenido.
——————————————–
Output:
(void*) Retorna un puntero al contenido del dato.
*/
void* getContenido(dato* d){
    return d->contenido;
}

/*
setContenido
Recibe un dato y un contenido, y le asigna este contenido al dato.
——————————————–
Inputs:
(dato*) Dato al que se le asignará el contenido.
(void*) Contenido que se asignará al dato.
——————————————–
Output:
(void) No retorna.
*/
void setContenido(dato* d, void* c){
    d->contenido = c;
}


void init(list* l){
    l->head = l->tail = l->actual = (node*)malloc(sizeof(node));
    l->tail->next = NULL;
    l->tail->info.contenido = NULL;
    l->tail->info.tipo = '\0';
    l->length = 0;
}

void clear(list* l){
    node* prev = l->head;
    l->actual = prev->next;
    while(l->actual != NULL){
        free_node(prev);
        prev = l->actual;
        l->actual = l->actual->next;
    }
    free_node(prev);
    l->head = l->tail = l->actual = NULL;
    l->length = 0;
    return;
}

void append(list* l, dato d){
    if(l->head == NULL) init(l);
    l->tail->next = (node*)malloc(sizeof(node));
    l->tail = l->tail->next;
    l->tail->info = copy_dato(d);
    l->tail->next = NULL;
    l->length++;
    return;
}

void insert(list* l, int i, dato d){
    if(l->head == NULL) init(l);
    if(i > l->length || i < 0) {printf("Indice invalido\n");return;}  //Invalid insert
    if(i == l->length) return append(l, d);
    l->actual = l->head;
    for(int pos = 0; pos < i; pos++)
        l->actual = l->actual->next;
    node* temp = l->actual->next;
    l->actual->next = (node*)malloc(sizeof(node));
    l->actual->next->info = copy_dato(d);
    l->actual->next->next = temp;
    l->length++;
    return;
}

void remov(list* l, int i){
    if(i >= l->length || l->length == 0 || i < 0) return;  //Invalid removes
    l->actual = l->head;
    for(int pos = 0; pos < i; pos++)
        l->actual = l->actual->next;
    if(i == l->length-1){ //Remove at tail
        l->tail = l->actual;
        free_node(l->actual->next);
        l->tail->next = NULL;
        l->length--;
        return;
    }
    node* temp = l->actual->next->next;
    free_node(l->actual->next);
    l->actual->next = temp;
    l->length--;
    return;
}

int length(list* l){
    return l->length;
}

dato* at(list* l, int i){
    if(i >= l->length || i < 0) return &(l->head->info);  //Invalid insert
    l->actual = l->head;
    for(int pos = 0; pos < i; pos++)
        l->actual = l->actual->next;
    return &l->actual->next->info;
}
