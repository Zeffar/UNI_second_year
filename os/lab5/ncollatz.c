#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>

int main(int argc, char *argv[])
{
    if (argc < 2)
        return EXIT_FAILURE;
    for (int i = 1; i < argc; ++i)
    {
        pid_t pid = fork();
        if (pid < 0)
            return -1;
        else if (pid == 0)
        {
            int num = atoi(argv[i]);
            printf("%d: ", num);
            while (num != 1)
            {
                if (num % 2)
                    num = 3 * num + 1;
                else
                    num /= 2;
                printf("%d ", num);
            }
            printf("\n");
            exit(EXIT_SUCCESS);
        }
    }
    for (int i = 1; i < argc; ++i)
    {
        int status;
        pid_t pid = wait(&status);
        if (pid > 0)
        {
            printf("Done Parent %d ME %d\n", getpid(), pid);
        }
    }

    return EXIT_SUCCESS;
}
