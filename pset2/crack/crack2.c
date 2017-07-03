#define _XOPEN_SOURCE
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>

int main (void)
{
    printf("%s\n", crypt("rofl", "50"));
}