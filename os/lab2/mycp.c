#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#define PAGESIZE 4096
int main(int argc, char *argv[])
{
    int fd = open(argv[1], O_RDONLY);
    int cd = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, S_IRWXU);
    char *buf = (char *)malloc(PAGESIZE * sizeof(char));
    ssize_t count;
    while ((count = read(fd, buf, PAGESIZE)) != 0)
        write(cd, buf, count);
    free(buf);
    return 0;
}