#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <string.h>

#define MAX_SEQUENCE 254

int main(int argc, char *argv[])
{
    if (argc < 2)
        return EXIT_FAILURE;

    const char *shm_name = "/collatz_shm";
    int shm_fd = shm_open(shm_name, O_CREAT | O_RDWR, 0666);
    if (shm_fd < 0)
    {
        perror("shm_open");
        return EXIT_FAILURE;
    }

    size_t shm_size = sizeof(int) * (MAX_SEQUENCE + 1) * (argc - 1);
    if (ftruncate(shm_fd, shm_size) == -1)
    {
        perror("ftruncate");
        close(shm_fd);
        shm_unlink(shm_name);
        return EXIT_FAILURE;
    }

    for (int i = 1; i < argc; ++i)
    {
        pid_t pid = fork();
        if (pid < 0)
        {
            perror("fork");
            return EXIT_FAILURE;
        }
        else if (pid == 0)
        {
            int *shm_ptr = (int *)mmap(NULL, shm_size, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
            if (shm_ptr == MAP_FAILED)
            {
                perror("mmap");
                exit(EXIT_FAILURE);
            }

            int num = atoi(argv[i]);
            int *local_ptr = shm_ptr + (i - 1) * (MAX_SEQUENCE + 1) + 1;
            *local_ptr = num;
            local_ptr++;
            int count = 1;

            while (num != 1 && count < MAX_SEQUENCE)
            {
                if (num % 2)
                    num = 3 * num + 1;
                else
                    num /= 2;

                *local_ptr = num;
                local_ptr++;
                count++;
            }
            *(shm_ptr + (i - 1) * (MAX_SEQUENCE + 1)) = count;

            munmap(shm_ptr, shm_size);
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

    int *shm_ptr = (int *)mmap(NULL, shm_size, PROT_READ, MAP_SHARED, shm_fd, 0);
    if (shm_ptr == MAP_FAILED)
    {
        perror("mmap");
        return EXIT_FAILURE;
    }

    for (int i = 1; i < argc; ++i)
    {
        int *local_ptr = shm_ptr + (i - 1) * (MAX_SEQUENCE + 1);
        int count = *local_ptr;
        local_ptr++;
        printf("%d: ", *local_ptr++);
        for (int j = 1; j < count; j++, local_ptr++)
        {
            printf("%d ", *local_ptr);
        }
        printf("\n");
    }

    munmap(shm_ptr, shm_size);
    close(shm_fd);
    shm_unlink(shm_name);

    return EXIT_SUCCESS;
}
