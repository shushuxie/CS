#### 测量系统调用和上下文切换的成本。测量系统调用的成本相对容 易。例如，你可以重复调用一个简单的系统调用（例如，执行 0 字节读取）并记下所花的 时间。将时间除以迭代次数，就可以估计系统调用的成本。



```c
#include <stdio.h>
#include <unistd.h>
#include <sys/file.h>
#include <sys/time.h>

int main() {
    // 结构体用来接收函数的值
    // timeval包含两部分，秒sec 和 微秒 usec；
    // s ms us
    struct timeval tv_end;
    struct timeval tv_start;

    // 打开文件，只读的形式；
    int fd = open("sysCallTime.txt",O_RDONLY);
    char *buf[2];
    gettimeofday(&tv_start,NULL);
    for (int i=0; i<1000000; i++)
    {
        read(fd,buf,0);
    }
    gettimeofday(&tv_end,NULL);
    float  sec =  tv_end.tv_sec-tv_start.tv_sec;
    float  usec = tv_end.tv_usec-tv_start.tv_usec;
    float  msec = sec*1000 + usec/1000;
    printf("read syscll use time =  %f s\n",sec);
    printf("read syscll use time = %f us\n",usec);
    printf("read total use time = %f ms\n",msec);
	  close(fd);

    return 0;
}


=======================================================
read syscll use time =  0.000000 s
read syscll use time = 226933.000000 us
read total use time = 226.932999 ms
一百万次调用平均每次调用耗时 0.22693299us；太快了

```

