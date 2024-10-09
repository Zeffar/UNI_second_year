#include <unistd.h>
int main()
{
    char v[] = "Hello world!\n";
    write(1, v, sizeof(v));
}