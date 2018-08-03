#include <cs50.h>
#include <stdio.h>

int get_negative_int();     // we declare our own function.

int main(void)
{
    int i = get_negative_int();                           // we want negative integer input from user. 
    printf("%i is a negative integer\n", i);          // whatever the user gives we print i is negative.

}
 int get_negative_int(void)                             //  we defining our own created function.
{
    int n;                                                        // when we see int n
    do                                                            // we do
    {
        printf("n is ");                                       // get an int from user        
        n = get_int();
    }                                                             
    while (n > 0);                                           // while  n > 0 
    return n;                                                  // WE DO WHAT ???
} 