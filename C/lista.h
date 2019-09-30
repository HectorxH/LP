#ifndef lista
#define lista

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

char getTipo(dato* d);

void setTipo(dato* d, char t);

void* getContenido(dato* d);

void setContenido(dato* d, void* c);

void init(list* a);

void clear(list* a);

void insert(list* a, int i, dato d);

void append(list* a, dato d);

void remov(list* a, int i);

int length(list* a);

dato* at(list*a, int i);

#endif
