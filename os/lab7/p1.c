#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define MAX_RESOURCES 5
#define THREADS 8

int available_resources = MAX_RESOURCES;
pthread_mutex_t mutex;

int decrease_count(int cnt)
{
    pthread_mutex_lock(&mutex);
    if (available_resources >= cnt)
    {
        available_resources -= cnt;
        printf("Got %d resources %d remaining\n", cnt, available_resources);
        pthread_mutex_unlock(&mutex);
        return 0;
    }
    else
    {
        pthread_mutex_unlock(&mutex);
        return -1;
        // not enough resources available
    }
}

void increase_count(int cnt)
{
    pthread_mutex_lock(&mutex);
    available_resources += cnt;
    printf("Released %d resources %d remaining\n", cnt, available_resources);
    pthread_mutex_unlock(&mutex);
}

void *request(void *arg)
{
    int count = rand() % 3 + 1; // ask for 1-3 resources
    while (decrease_count(count) == -1)
        ; 
    usleep(100000);
    increase_count(count);
    return NULL;
}

int main(int argc, char *argv[])
{
    pthread_t threads[THREADS];
    pthread_mutex_init(&mutex, NULL);
    printf("MAX RESOURCES = %d\n", MAX_RESOURCES);

    for (int i = 0; i < THREADS; ++i)
        pthread_create(&threads[i], NULL, request, NULL);

    for (int i = 0; i < THREADS; ++i)
        pthread_join(threads[i], NULL);

    pthread_mutex_destroy(&mutex);
    return EXIT_SUCCESS;
}