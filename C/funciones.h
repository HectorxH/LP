#ifndef funciones
#define funciones

struct list;
struct data;

typedef struct list list;
typedef struct data data;

list* map(struct list* l, data (*f)(data));

float sum(list* l);

void print(list* l);

float averge(list* l);

#endif
