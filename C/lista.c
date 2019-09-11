#include "lista.h"

struct data{
    void* contenido;
    char tipo;
};

struct node{
    data info;
    node* next;
};

struct list{
    node* actual;
    node* head;
    node* tail;
    int length;
};
