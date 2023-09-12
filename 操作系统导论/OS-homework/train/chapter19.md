
1. 假设分页2KB
2. CPU未进行绑定
3. 没有做图
   

```
#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
#include <pthread.h>


float time_diff(struct timeval *start, struct timeval *end)
{
    return (end->tv_sec - start->tv_sec) + 1e-6*(end->tv_usec - start->tv_usec);
}


int main() {
    struct timeval start;
    struct timeval end;

    int NUMPAGES = 1;
    for (int h = 1; h < 8; h++) {
        gettimeofday(&start, NULL);
        int PAGESIZE = 1024*2;
        NUMPAGES *= 2;
        int jump = PAGESIZE / sizeof(int);
        int a[NUMPAGES*jump] ;
        for (int j = 0; j < 100000000; j++) {
            for (int i = 0; i < NUMPAGES * jump; i += jump) {
                a[i] += 1;
            }
        }
        gettimeofday(&end, NULL);

        printf("loopFunc NumPages=%d time spent: %0.8f ns\n",
               NUMPAGES, time_diff(&start, &end));
    }

    exit(EXIT_SUCCESS);
}
```
