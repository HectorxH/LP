#include "funciones.h"
#include "lista.h"
#include <stdio.h>

typedef struct list list;
typedef struct node node;
typedef struct dato dato;

list* map(list* a, dato (*f)(dato)){
    int i;
    int len = length(a);
    for (i=0; i<len; i++){
        dato* d = at(a, i);
        char tipo_d = d->tipo;
        if(tipo_d == 'l')
            d->contenido = map((list*)d->contenido, f);
        else if(tipo_d == 'i' || tipo_d == 'f')
            *d = f(*d);
    }
    return a;
}

<<<<<<< HEAD
float sum(struct list* a){
  int i;
  float total = 0;
  int len = lenght(a);
  for (i=0; i<len; i++){
    struct dato = at(a, i);
    char tipo_d = dato.tipo;
    void* cont_d = dato.contenido;
    if(tipo_d == 'l'){
      total += sum((struct list*)cont_d);
    }
    else if(tipo_d == 'i'){
      total += (int)cont_d;
=======
float sum(list* a){
    int i;
    float total = 0;
    int len = length(a);
    for (i=0; i<len; i++){
        dato* d = at(a, i);
        char tipo_d = d->tipo;
        if(tipo_d == 'l')
            total += sum((list*)d->contenido);
            else if(tipo_d == 'i')
            total += *((int*)d->contenido);
        else if(tipo_d == 'f')
            total += *((float*)d->contenido);
>>>>>>> 2fd842f865e60883e815eefa5facd38d0e831953
    }
    return total;
}

void print_aux(list* a){
    int i;
    int len = length(a);
    printf("[");
    for(i=0; i<len; i++){
        dato* d = at(a, i);
        char tipo_d = d->tipo;
        if(tipo_d == 'l')
            print((list*)d->contenido);
        else if(tipo_d == 'i')
            printf("%d", *((int*)d->contenido));
        else if(tipo_d == 'f')
            printf("%f", *((float*)d->contenido));
        if (i != len-1)
            printf(", ");
    }
    printf("]");
    return;
}

void print(struct list* a){
<<<<<<< HEAD
  int i, entero;
  int len = lenght(a);
  float flotante;
  printf("[");
  for(i=0; i<len; i++){
    struct dato = at(a, i);
    char tipo_d = dato.tipo;
    void* cont_d = dato.contenido;
    if(tipo_d == 'l'){
      print((struct list*)cont_d);
    }
    else if(tipo_d == 'i'){
      entero = (int)cont_d;
      printf("%d", &entero);
    }
    else if(tipo_d == 'f'){
      flotante = (float)cont_d;
      printf("%f", &flotante);
    }
    i++;
  }
  printf("]\n");
  return;
}

float average(struct list* a){
  int i;
  int len = lenght(a);
  float suma = 0;
  float prom;
  for (i=0; i<len; i++){
    struct dato = at(a, i);
    char tipo_d = dato.tipo;
    void* cont_d = dato.contenido;
    if(tipo_d == 'l'){
      suma += average((struct list*)cont_d);
    }
    else if(tipo_d == 'i'){
      suma += (int)cont_d;
    }
    else if(tipo_d == 'f'){
      suma += (float)cont_d;
=======
    int i;
    int len = length(a);
    printf("[");
    for(i=0; i<len; i++){
        dato* d = at(a, i);
        char tipo_d = d->tipo;
        if(tipo_d == 'l')
            print_aux((list*)d->contenido);
        else if(tipo_d == 'i')
            printf("%d", *((int*)d->contenido));
        else if(tipo_d == 'f')
            printf("%f", *((float*)d->contenido));
        if (i != len-1)
            printf(", ");
    }
    printf("]\n");
    return;
}

float average(struct list* a){
    int i, n, len;
    n = len =length(a);
    float suma = 0;
    for (i=0; i<len; i++){
        dato* d = at(a, i);
        char tipo_d = d->tipo;
        if(tipo_d == 'l')
            if(length((list*)d->contenido) == 0) n--;
            else suma += average((list*)d->contenido);
        else if(tipo_d == 'i')
            suma += *((int*)d->contenido);
        else if(tipo_d == 'f')
            suma += *((float*)d->contenido);
>>>>>>> 2fd842f865e60883e815eefa5facd38d0e831953
    }
    return suma/len;
}
