#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
int THREADS;
int counter = 0;
pthread_mutex_t mutex;
pthread_cond_t cond;

void init(int n)
{
    THREADS = 8;
    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&cond, NULL);
}

void barrier_point()
{
    pthread_mutex_lock(&mutex);
    counter++;
    if (counter == THREADS)
    {
        counter = 0;
        pthread_cond_broadcast(&cond);
    }
    else
    {
        pthread_cond_wait(&cond, &mutex);
    }
    pthread_mutex_unlock(&mutex);
}

void *tfun(void *v)
{
    int *tid = (int *)v;
    printf("%d reached the barrier\n", *tid);
    barrier_point();
    printf("%d passed the barrier\n", *tid);
    free(tid);
    return NULL;
}

int main(int argc, char *argv[])
{
    init(8);
    pthread_t threads[THREADS];

    for (int i = 0; i < THREADS; ++i)
    {
        int *tid = malloc(sizeof(int));
        *tid = i + 1;
        pthread_create(&threads[i], NULL, tfun, tid);
    }

    for (int i = 0; i < THREADS; ++i)
        pthread_join(threads[i], NULL);

    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cond);
    return EXIT_SUCCESS;
}