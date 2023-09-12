#### 1．编写一个调用 fork()的程序。谁调用 fork()之前，让主进程访问一个变量（例如 x） 并将其值设置为某个值（例如 100）。子进程中的变量有什么值？当子进程和父进程都改变 x 的值谁，变量会发生什么？

分析：父进程和子进程分别独立使用x变量；子进程接收到的x值是父进程在fork之前的最后结果，子进程后面改变x的值不会影响父进程的结果；

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h> 

int main(){
	int x = 0;
	printf(" parent init x = %d \n",x);
	x = 100;
	printf(" parent before fork set value x = %d \n",x);
	int result = fork();
		if (result == 0){
		printf("child befor set x = %d\n",x);
		x = 200;
		printf("child set x = %d \n",x);
	} else {
		int wc = wait(NULL);
		printf("parent after x = %d \n",x);
}

	return 0;

}

// 输出结果
parent init x = 0 
parent before fork set value x = 100 
child befor set x = 100
child set x = 200 
parent after x = 100  //即使等待子进程结束，父进程仍然不受影响
```

#### 2．编写一个打开文件的程序（使用 open()系统调用），然后调用 fork()创建一个新进程。 子进程和父进程都可以访问 open()返回的文件描述符吗？当它并发（即同时）写入文件时， 会发生什么？

分析：出乎意料，父进程和子进程都可以访问文件；同时写入会发生争夺；

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h> 
#include <sys/types.h>
#include <fcntl.h>

int main(){

	int f = open("./file.txt",O_WRONLY|O_APPEND);
    printf("file description = %d\n",f);

    int fk = fork();
    if (fk < 0) {
        fprintf(stderr,"child process create fail");
    } else if (fk == 0) {
        printf("child get file handle f=%d\n",f);

        int a = write(f,"child write",12);
        if (a > 0) {
            printf("child write success ");
        } else {
            printf("child write fail");
        }
    } else {
        int w = write(f,"parent write",12);
        printf("file write return = %d\n",w);
    }
    close(f);

	return 0;
}
// 结果是两个进程都写入了数据，
// 原因应该是文件描述符独立于线程，只要文件打开谁拿到文件描述符都可以操作文件；

```





#### 3．使用 fork()编写另一个程序。子进程应打印“hello”，父进程应打印“goodbye”。你 应该尝试子进程始终先打印。你能否不在父进程调用 wait()而做到这一点呢？

分析：这样估计应该要是线程睡眠才行

```c
#include <stdio.h>
#include <unistd.h>
#include<sys/types.h>
#include <fcntl.h>
int main() {
	int i = 0;
        int rc = fork();
        if (rc < 0) {
            fprintf(stderr,"child create fail");
        } else if(rc == 0){
            printf("hello");
        } else {
	    sleep(1);
            printf("goodbye;\n");
        }

    return 0;
}


```





#### 4．编写一个调用 fork()的程序，然后调用某种形式的 exec()来运行程序/bin/ls。看看是 否可以尝试 exec()的所有变体，包括 execl()、execle()、execlp()、execv()、execvp()和 execvP()。为什么同样的基本调用会有这谁多变种？

分析：fork子进程中调用别的程序就会阻拦exec函数后面的执行，相当于子进程映射为另一个函数，是同一个pid；

这么多变种是方便使用；

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

void myprint();

void myprint() {
    printf("my prient %s");
}

int main() {

     int rc = fork();
     char *path = "/Users/xieshuqiang/Documents/typora/操作系统导论/OS-homework/myprient";
     if (rc < 0) { // fork failed; exit
         fprintf(stderr, "fork failed\n");
         exit(1);
     } else if (rc == 0) { // child (new process)
         printf("hello, I am child (pid:%d)\n", (int) getpid());
         char *myargs[2];
         myargs[0] = strdup(path); // 第一个参数执行的文件名，执行ls，填入ls即可，或者/bin/ls
         myargs[1] = strdup("mains"); // 文件需要接收的参数
         myargs[2] = NULL; // 最后一位是NULL指针

         // 第二个参数是数组
         execvp(myargs[0], myargs); // runs word count
        // exec函数家族，后面接收单个参数，以单个char* 出现
//         execl(path,"myprient",NULL);
         printf("this shouldn't print out");
     } else { // parent goes down this path (main)
         int wc = wait(NULL);
         printf("hello, I am parent of %d (wc:%d) (pid:%d)\n",
                 rc, wc, (int) getpid());
         }


    return 0;
}
```



#### 5．现在编写一个程序，在父进程中使用 wait()，等待子进程完成。wait()返回什么？如 果你谁在子进程中使用 wait()会发生什么？ 

> 分析：wait成功返回子进程的pid，失败返回-1，子进程没有可以等待的进程返回-1

```c
int main() {

     int rc = fork();
     if (rc < 0) { // fork failed; exit
         fprintf(stderr, "fork failed\n");
         exit(1);
     } else if (rc == 0) { // child (new process)
         int wc = wait(NULL);
         printf("hello, I am child (pid:%d) (c-wait:%d)\n",(int) getpid(),wc);

     } else { // parent goes down this path (main)
         int wc = wait(NULL);
         printf("hello, I am parent of %d (wait:%d) (pid:%d)\n",
                 rc, wc, (int) getpid());
         }


    return 0;
}

/** print result **/
hello, I am child (pid:78213) (c-wait:-1)
hello, I am parent of 78213 (wait:78213) (pid:78211)
```



####  6．对前一个程序稍作修改，这次使用 waitpid()而我是 wait()。什么时候 waitpid()会 有用？

> waitpid可以等待别的进程；可以让子进程等待特定的进程组或者别的单个进程；也可以不等待进程结束；





####  7．编写一个创建子进程的程序，然后在子进程中关闭标准输出（STDOUT_FILENO）。 如果子进程在关闭描述符后调用 printf()打印输出，会发生什么？

> 关闭后后续输出无法进行；

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {

     int rc = fork();
     if (rc < 0) { // fork failed; exit
         fprintf(stderr, "fork failed\n");
         exit(1);
     } else if (rc == 0) { // child (new process)
         printf("hello, I am child (pid:%d)\n",(int) getpid());
         close(STDOUT_FILENO); // 关闭标准输出
         printf("clos STDOUT after print \n");

     } else { // parent goes down this path (main)
         printf("hello, I am parent of %d (wait:%d) (pid:%d)\n",
                 rc, (int) getpid());
         }


    return 0;
}

/*******************************************************/
hello, I am parent of 81519 (wait:81516) (pid:81519)
hello, I am child (pid:81519)
```





####  8．编写一个程序，创建两个子进程，并使用 pipe()系统调用，将一个子进程的标准输 出连接到另一个子进程的标准输入。



```c
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUF_SIZE 256
// 父进程和子进程pipe
int main() {
    int pipefd[2];
    char buf[BUF_SIZE];
    pid_t pid;

    if (pipe(pipefd) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    pid = fork();
    if (pid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    }

    if (pid == 0) { // child process
        close(pipefd[0]); // close the read end of the pipe
        strcpy(buf, "Hello, parent process!\n");
        write(pipefd[1], buf, strlen(buf));
        close(pipefd[1]); // close the write end of the pipe
        exit(EXIT_SUCCESS);
    } else { // parent process
        close(pipefd[1]); // close the write end of the pipe
        while (read(pipefd[0], buf, BUF_SIZE) > 0) {
            printf("Received message: %s", buf);
        }
        close(pipefd[0]); // close the read end of the pipe
        exit(EXIT_SUCCESS);
    }
}

```



```c
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUF_SIZE 256
// 子进程之间pipe
int main() {
    int pipefd[2];
    char buf[BUF_SIZE];
    pid_t pid,pid2;

    if (pipe(pipefd) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    pid = fork();
    if (pid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    }

    if (pid == 0) { // child process
        close(pipefd[0]); // close the read end of the pipe
        strcpy(buf, "Hello,  child2 process!\n");
        write(pipefd[1], buf, strlen(buf));
        close(pipefd[1]); // close the write end of the pipe
        exit(EXIT_SUCCESS);
    } else {// parent process
        
	pid2 = fork();
	if(pid2 == 0){
		close(pipefd[1]); // close the write end of the pipe
		while (read(pipefd[0], buf, BUF_SIZE) > 0) {
		    printf("Received message: %s", buf);
		}
			close(pipefd[0]); // close the read end of the pipe
			exit(EXIT_SUCCESS);
		}


    }
return 0;

}

```

