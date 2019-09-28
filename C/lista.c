#include <stdlib.h>
#include <stdio.h>
#include "lista.h"

typedef struct list list;
typedef struct node node;
typedef struct dato dato;

/*
free_node
Función que libera la memoria de un nodo.
——————————————–
Inputs:
(node*) Nodo al que se le liberará la memoria.
——————————————–
Output:
(void) No retorna.
*/

void free_node(node* n){
    if(n->info.tipo == 'l') clear((list*)n->info.contenido);
    free((void*)n);
}

dato copy(dato d){
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
    l->tail->info = copy(d);
    l->tail->next = NULL;
    l->length++;
    return;
}

void insert(list* l, int i, dato d){
    if(l->head == NULL) init(l);
    if(i > l->length || i < 0) return;  //Invalid insert
    if(i == l->length) return append(l, d);
    l->actual = l->head;
    for(int pos = 0; pos < i; pos++)
        l->actual = l->actual->next;
    node* temp = l->actual->next;
    l->actual->next->info = copy(d);
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
