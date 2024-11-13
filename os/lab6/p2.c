#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

#define N 3

typedef struct
{
    int row, col, (*A)[N], (*B)[N], (*C)[N];
} Data;

void mulmat(int A[N][N], int B[N][N], int C[N][N])
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            C[i][j] = 0;
            for (int k = 0; k < N; k++)
            {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

void *mul(void *arg)
{
    Data *data = (Data *)arg;
    int row = data->row;
    int col = data->col;

    data->C[row][col] = 0;
    for (int k = 0; k < N; k++)
    {
        data->C[row][col] += data->A[row][k] * data->B[k][col];
    }
    return NULL;
}

int main(int argc, char *argv[])
{
    int A[N][N] = {
        {1, 2, 3},
        {2, 3, 4},
        {3, 4, 5}};

    int B[N][N] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}};

    int C[N][N];

    pthread_t threads[N][N];
    Data thread_data[N][N];

    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j)
        {
            thread_data[i][j].row = i;
            thread_data[i][j].col = j;
            thread_data[i][j].A = A;
            thread_data[i][j].B = B;
            thread_data[i][j].C = C;

            if (pthread_create(&threads[i][j], NULL, mul, &thread_data[i][j]) != 0)
            {
                return EXIT_FAILURE;
            }
        }

    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            if (pthread_join(threads[i][j], NULL) != 0)
            {
                return EXIT_FAILURE;
            }
        }
    }

    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            printf("%d ", C[i][j]);
        }
        printf("\n");
    }
    return EXIT_SUCCESS;
}