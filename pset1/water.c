#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int x;
    int y;
    
    printf("Input the shower's length in minutes: ");
    
    x = get_int();
    
    //x = min*192;
    
    y = (x*192)/16;
    
    printf("Minutes: %i\n", x);
    printf("Bottles: %i\n", y);
}