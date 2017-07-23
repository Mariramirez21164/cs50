#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

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
    char name[8];

    int k = 0;
    int i = 0;    

    do
    {
        // Read 512 blocks of size 1 byte FROM inptr and send it to &block
        i = fread(&block, 1, 512, inptr);
        
        // JPEG signature condition
        if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xf0) == 0xe0)
        {
            // Create variable "name" with "00k.jpg"
            sprintf(name, "%03i.jpg", k);
            k++;
            // Create file "name" with write permission
            FILE *outptr = fopen(name, "w");
            
            // Inside this loop the image is "created"
            do
            {
                // Write result to file
                fwrite(&block, 1, 512, outptr);
                
                i = fread(&block, 1, 512, inptr);
                
                // A wild block appears!
                if(i != 512)
                {
                    break;
                }
                
            } // If the block red is a JPEG signature GTFO
            while (block[0] != 0xff || block[1] != 0xd8 || block[2] != 0xff || (block[3] & 0xf0) != 0xe0);
            
            // Close image
            fclose(outptr);
        
            // IT TURNS OUT THAT YOU JUST READED THE JPEG SIGNATURE AND YOU GOTTA GET BACK SO WHEN THE LOOP STARTS
            // AGAIN, IT RECOGNIZES THE JPEG AND CREATES THE IMAGE
            fseek(inptr, -(512), SEEK_CUR);
            
        }
        
    }
    while (i == 512);

}
