#include <stdio.h>
#include <cs50.h>

int main (void)
{
    printf("Put your credit card number without spaces: \n");
    long long n = get_long_long();
    
    while(n<=0){
        printf("Please, retry a valid number: \n");
        n = get_long_long();
    }
    
    
        int a = n % 10;
        a = a / 1;
        int b = n % 1000;
        b = b / 100;
        int c = n % 1000000;
        c = c / 100000;
        long long d = n % 100000000;
        d = d / 10000000;
        long long e = n % 10000000000;
        e = e / 1000000000;
        long long f = n % 1000000000000;
        f = f / 100000000000;
        long long g = n % 100000000000000;
        g = g / 10000000000000;
        long long h = n % 10000000000000000;
        h = h / 1000000000000000;
        
        printf("%d\n", a);
        printf("%d\n", b);
        printf("%d\n", c);
        printf("%lld\n", d);    
        printf("%lld\n", e);
        printf("%lld\n", f);
        printf("%lld\n", g);
        printf("%lld\n", h);
    
}