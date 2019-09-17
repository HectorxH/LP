#include "funciones.h"

typedef struct list list;
typedef struct node node;
typedef struct dato data;

list* map(list* l, data (*f)(dato)){
    return l;
}

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
    }
    else if(tipo_d == 'f'){
      total += (float)cont_d;
    }
    i++;
  }
  return total;
}

void print(struct list* a){
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
    }
    i++;
  }
  prom = suma/len;
  return prom;
}
