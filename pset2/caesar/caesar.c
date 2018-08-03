#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main (int argc, string argv[])
{

    if (argc == 2)
    {
        int k = atoi(argv[1]);
    
        printf("Plaintext: ");
        string s = get_string();
        
        for(int i = 0, n = strlen(s); i < n; i++)
        {
            if (isalpha (s[i]))
            {
                if (isupper (s[i]))
                {
                    if (k<26)
                    {
                        s[i] = (s[i] + k);
                    }
                    else
                    {
                        s[i] = s[i] + (k % 26);
                    }
                }
                else if (islower (s[i]) )
                {
                    if (k<26)
                    {
                        s[i] = (s[i] + k);
                    }
                    else
                    {
                        s[i] = s[i] + (k % 26);
                    }
                }
            }
            else
            {
                s[i] = s[i];
            }
        }
        printf("ciphertext: %s\n", s);
        
    }
    else
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }

    

}