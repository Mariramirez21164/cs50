#define _XOPEN_SOURCE
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>

int main (int argc, string argv[])
{

    string hash = NULL;
    
    if (argc == 2)
    {
        hash = argv[1]; // Store hashed pass in "hash"
    }
    else
    {
        printf("Usage: ./crack k\n");
        return 1;
    }
    
//    int salt = 50; // Already given
    
    printf("%s\n", hash);    

    /*  strcmp
        Hashear cada pass con crypt()
        Comparar hash con string s
        Si es igual printf pass
    */
}