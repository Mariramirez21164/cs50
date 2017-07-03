/**
 * generate.c
 *
 * Generates pseudorandom numbers in [0,MAX), one per line.
 *
 * Usage: generate n [s]
 *
 * where n is number of pseudorandom numbers to print
 * and s is an optional seed
 */
 
#define _XOPEN_SOURCE

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// upper limit on range of integers that can be generated
#define LIMIT 65536

int main(int argc, string argv[])
{
    // TODO: Si la cant. de argumentos no corresponde a 2 o 3, return 1.
    if (argc != 2 && argc != 3)
    {
        printf("Usage: ./generate n [s]\n");
        return 1;
    }

        // TODO: Convierto el segundo argumento (string) en un (int) mediante "atoi" y lo asigno a "n".
    
    int n = atoi(argv[1]);

        // TODO: Si se encuentra un tercer argumento, se convierte a (int) mediante "atoi". Este int  
        // a su vez es tomado como long y se utiliza como el argumento de "srand48".
        // Es la semilla utilizada para drand48
    
        // Si no se encuentra tercer argumento, se utiliza time(NULL) que devuelve un valor nulo pero válido.
    
    if (argc == 3)
    {
        srand48((long) atoi(argv[2]));
    }
    else
    {
        srand48((long) time(NULL));
    }

        // TODO: Repite el proceso (n-1) veces siendo n el segundo arg del programa.
        // 
    
    for (int i = 0; i < n; i++)
    {
        printf("%i\n", (int) (drand48() * LIMIT));
    }

    // success
    return 0;
}
