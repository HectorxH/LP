#ifndef funciones
#define funciones

struct dato{
    void* contenido;
    char tipo;
};

struct node{
    struct dato info;
    struct node* next;
};

struct list{
    struct node* actual;
    struct node* head;
    struct node* tail;
    int length;
};

typedef struct list list;
typedef struct node node;
typedef struct dato dato;

list* map(struct list* l, dato (*f)(dato));

float sum(list* l);

void print(list* l);

float averge(list* l);

#endif
