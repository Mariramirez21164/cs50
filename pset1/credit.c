#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main (void)
{
    printf("Put your credit card number without spaces: \n");
    long long n = get_long_long();
    
    while(n<=0){
        printf("Please, retry a valid number: \n");
        n = get_long_long();
    }
    
    long long b = 100;
    long long d = 10;
//    int e = 0;
  //  string card;
    int sum = 0;
    while(b<=10000000000000000)
    {   long long a = n % b;    //Guarda los n° con paso 2 desde el penúltimo hacia atrás en a
        a = a / (b/10);
        
        long long c = n % d;    //Guarda los n° con paso 2 desde el último hacia atrás en c
        c = c / (d/10);
        
        printf("%lld\n", a);
        printf("%lld\n", c);
        
        a = a * 2;
        
        if(a>9)
        {
            sum = sum + a % 10;
            sum = sum + a / 10;
        }    
        else
        {
            sum = sum + a;
        }
        
        
        sum = sum + c;
        
        b = b*100;
        d = d*100;
    }
    
        printf("%d\n", sum);
        printf("%lu\n", strlen(n));
    if((sum % 10) == 0)
    {
        printf("");
    }
}
