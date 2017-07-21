#include <stdio.h>
#include <stdlib.h>

#include "jpeg.h"

int main (int argc, char *argv[])
{
    // argc check
    if (argc != 2)
    {
        fprintf(stderr, "Uso: ./recover file");
        return 1;
    }
    
    // Remember filenames
    char *infile = argv[1];
    
    // Open infile
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "%s no puede abrirse en modo lectura\n", infile);
        return 2;
    }
    
    // BYTE(unsigned int) array
    BYTE block [512];

    int i = 0;
    while( i < 3)
    {
        // Save the result of fread in k
        int k = fread(&block, 1, 512, inptr);
        
        // JPEG signature condition
        if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xf0) == 0xe0)
        {
                // Create asd.txt with write permission
                FILE *outptr = fopen("asd.jpg", "w");
            
            do
            {
                // Write result to asd.jpg
                fwrite(&block, 1, 512, outptr);
            
                k = fread(&block, 1, 512, inptr);
                
            }
            while (block[0] != 0xff || block[1] != 0xd8 || block[2] != 0xff || (block[3] & 0xf0) != 0xe0);
        }
    
    // Write the result to asd.txt
//    
    
        // Test only
        printf("%d\n", k);
        printf("%d\n", block[50]);
    
        i++;
    }

    
}