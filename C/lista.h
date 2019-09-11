#ifndef lista
#define lista

typedef struct list list;
typedef struct node node;
typedef struct data data;

void init(list* l);

void clear(list* l);

void insert(list* l, int i, data d);

void append(list* l, data d);

void remv(list* l, int i);

int length(list* l);

data* at(list*l, int i);

#endif
