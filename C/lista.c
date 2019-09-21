#include <stdlib.h>
#include <stdio.h>
#include "lista.h"

typedef struct list list;
typedef struct node node;
typedef struct dato dato;

void free_node(node* n){
    //if(n->info.tipo == 'l') clear((list*)n->info.contenido);
    free((void*)n);
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
    return;
}

void append(list* l, dato d){
    l->tail->next = (node*)malloc(sizeof(node));
    l->tail = l->tail->next;
    l->tail->info.contenido = d.contenido;
    l->tail->info.tipo = d.tipo;
    l->tail->next = NULL;
    l->length++;
    return;
}

void insert(list* l, int i, dato d){
    if(i > l->length || i < 0) return;  //Invalid insert
    if(i == l->length) return append(l, d);
    l->actual = l->head;
    for(int pos = 0; pos < i; pos++)
        l->actual = l->actual->next;
    node* temp = l->actual->next;
    l->actual->next = (node*)malloc(sizeof(node));
    l->actual->next->info.contenido = d.contenido;
    l->actual->next->info.tipo = d.tipo;
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
