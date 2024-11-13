#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

void *strrev(void *arg)
{
    char *data = (char *)arg;
    int len = strlen(data);
    char *output = (char *)malloc(len + 1);
    for (int i = 0; i < len; i++)
    {
        output[i] = data[len - i - 1];
    }
    output[len] = '\0';
    return output;
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return EXIT_FAILURE;
    }

    char *input = argv[1];
    int len = strlen(input);
    pthread_t thread;

    if (pthread_create(&thread, NULL, strrev, input) != 0)
        return EXIT_FAILURE;

    void *output;
    if (pthread_join(thread, &output) != 0)
        return EXIT_FAILURE;

    output = (char *)output;
    printf("%s\n", output);
    free(output);

    return EXIT_SUCCESS;
}