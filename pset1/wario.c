#include <stdio.h>
#include <cs50.h>


int main (void)
{
    printf("Input the pyramid's height: ");

    int a, b, c, n = get_int();
    while(n<0 || n>23){
        
        printf("Error. Please input again: ");
        n = get_int();
        }
   
    for(a=0; a<n; a++)
    {
        for(b=1; b<(n-a); b++)
        {
            printf(" ");
        }
        for(c=1; c<(a+2); c++)
        {
            printf("#");
        }
        printf("  ");
        for(c=1; c<(a+2); c++)
        {
            printf("#");
        }
        printf("\n");
    }
    return 0;
}