#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main (void)
{
    printf("Input your full name: ");
    string s = get_string();
    
    for (int i = 0, n = strlen(s); i < n; i++)
    {

        if (s[i] != ' ')
        {
            if (i == 0)
            {
                printf("%c\n", toupper(s[i]));
            }
            else if (s[i-1] == ' ' && s[i+1] != ' ')
            {
                printf("%c\n", toupper(s[i]));
            }
            
        }
    }
}