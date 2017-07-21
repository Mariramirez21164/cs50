#include <stdio.h>

int main(void)
{
    char buffer[50];

    int course = 40;

    sprintf(buffer,"CS%d rocks!", course);

    printf("%s\n", buffer);
}