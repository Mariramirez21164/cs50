/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm
    int min = 0;
    int med = 0;
    int max = n - 1;
    
    if (n > 0)
    {
        while (min <= max)
        {
            med = (min + max)/2;
            
            if (values[med] == value)
            {
                return 0;
            }
            else if (values[med] > value)
            {
                max = med - 1;
            }
            else
            {
                min = med + 1;
            }
        }
        return 0;
    }
    else
    {
        return 0;
    }
        
}

/**
 * Sorts array of n values.
 */

void sort(int values[], int n)
{
    int index[65535] = {0};
    
    for(int i = 0; i < n; i++)
    {
        int j = values[i];              // Recorro values[] y guardo el valor en j.
        index[j] = index[j] + 1;        // Sumo +1 en cada posición de index[j].
    }
    
    int m = 0;
    
    for(int k = 0; k <= 65535; k++)
    {
        while(index[k] != 0)            // Verifico el valor de index[k] hasta que sea 0
        {
            values[m] = k;              // Guardo en values[m] el valor de k (representa el n° ordenado)
            m++;                        // Una vez guardado paso al siguiente casillero de values
            index[k] = index[k] - 1;    // Resto el valor de index[k] por si hay n° repetidos
        }
    }
    
    
    return;
}
