#ifndef funciones
#define funciones

typedef struct list list;
typedef struct node node;
typedef struct dato dato;

list* map(struct list* l, dato (*f)(dato));

float sum(list* l);

void print(list* l);

float average(list* l);

#endif
