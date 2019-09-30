Héctor Larrañaga    201873623-6
Sofía Palet         201873570-1

Se asume que:
* Los datos ingresados en la lista son copiados.
* Las listas retornadas por la función map son liberadas por el usuario.
* Si se realiza una inserción a una lista en una posición mayor a la última
  existente, se realizará la función append.
* Si el promedio de una lista no está definido, la función average imprime
  "Error: El promedio no está definido para esta lista." en la consola cada vez
  que ocurra y retornará un valor erróneo.
* La función init recibe una lista de la forma:
    list l;
    init(&l);
* La implementación del TDA incluye las siguientes definiciones para tipos:
    typedef struct list list;
    typedef struct node node;
    typedef struct dato dato;
* El archivo main.c contiene la función int main()
* El archivo Makefile genera como salida el archivo main.out
* Makefile compila con las siguientes flags:
    -Wall -Wextra -Wpointer-arith -g -std=c99
