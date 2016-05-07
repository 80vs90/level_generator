#include <stdio.h>

int main()
{
    FILE *f = NULL;
    int i;

    f = fopen("test_level.bin", "rb");
    if (f == NULL)
    {
        printf("Error opening file.");
        return 1;
    }
    while(!feof(f))
    {
        fread(&i, sizeof(int), 1, f);
        printf("%d\n", i);
    }

    fclose(f);
    return 0;
}
