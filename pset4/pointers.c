//https://youtu.be/ywqB3ZTf8OE?t=583

#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int m;
    int* a; // Defino un pointer "a" que tendrá la dirección de un int
    int* b = malloc(sizeof(int)); // Defino un pointer "b" y le asigno un espacio de 4 bytes (int)
    a = &m; // Guardo la dirección de "m" en "a"
    a = b;  // "a" apunta al mismo espacio que "b"
    m = 10;
    *b = m + 2; //DEREFERENCE. Ponemos (m+2) en el espacio al que apunta "b"
    free(b);
//    *a = 11;
    
    
    printf("a equals %p\n", (void *) &a);
    printf("b equals %p\n", (void *) &b);
    printf("m equals %i\n", m);
}