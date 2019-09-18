#include <stdlib.h>
#include "lista.h"

typedef struct list list;
typedef struct node node;
typedef struct dato dato;

void init(list* l){
    l->head = l->tail = l->actual = (node*)malloc(sizeof(node));
    l->tail->next = NULL;
    l->tail->info.contenido = NULL;
    l->tail->info.tipo = '\0';
    l->length = 0;
}

void clear(list* l){
    if(l->length == 0){
        free((void*)l->head);
        return free((void*)l);
    }
    node* prev = l->head;
    l->actual = prev->next;
    while(l->actual != l->tail){
        if(prev->info.tipo == 'l') clear((list*)prev->info.contenido);
        else free((void*)prev->info.contenido);
        free((void*)prev);
        prev = l->actual;
        l->actual = l->actual->next;
    }
    free((void*)l->actual);
    return free((void*)l);
}

void insert(list* l, int i, dato d){
    if(i >= l->length || i < 0) return;  //Invalid insert
    l->actual = l->head;
    for(int pos = 0; pos < i; i++)
        l->actual = l->actual->next;
    node* temp = l->actual->next;
    l->actual->next = (node*)malloc(sizeof(node));
    l->actual->next->info.contenido = d.contenido;
    l->actual->next->info.tipo = d.tipo;
    l->actual->next->next = temp;
    l->length++;
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

void remove(list* l, int i){
    if(i >= l->length || l->length == 0 || i < 0) return;  //Invalid removes
    l->actual = l->head;
    for(int pos = 0; pos < i; i++)
        l->actual = l->actual->next;
    if(i == l->length-1){ //Remove at tail
        l->tail = l->actual;
        if(l->actual->next->info.tipo == 'l') clear((list*)l->actual->next->info.contenido);
        else free(l->actual->next->info.contenido);
        free((void*)l->actual->next);
        l->length--;
        return;
    }
    node* temp = l->actual->next->next;
    if(l->actual->next->info.tipo == 'l') clear((list*)l->actual->next->info.contenido);
    else free(l->actual->next->info.contenido);
    free((void*)l->actual->next);
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
    for(int pos = 0; pos < i; i++)
        l->actual = l->actual->next;
    return &(l->actual->next->info);
}
