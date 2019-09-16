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
typedef struct dato data;

void init(list* l);

void clear(list* l);

void insert(list* l, int i, data d);

void append(list* l, data d);

void remv(list* l, int i);

int length(list* l);

data* at(list*l, int i);

#endif
