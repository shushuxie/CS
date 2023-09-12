#### 1．首先，编写一个名为 null.c 的简单程序，它创建一个指向整数的指针，将其设置为 NULL，然后尝试对其进行释放内存操作。把它编译成一个名为 null 的可执行文件。当你运 行这个程序时会发生什么？

运行没有错误，直接结束，free可以释放malloc，clloc，realloc申请的内存，NULL指针也可以；

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *x = NULL;
    free(x);
    return 0;
}
```



####  2．接下来，编译该程序，其中包含符号信息（使用-g 标志）。这样做可以将更多信息 放入可执行文件中，使调试器可以但问有关变量名称等的更多有用信息。通过输入 gdb null， 在调试器下运行该程序，然后，一旦 gdb 运行，输入 run。gdb 显示什么信息？ 

```c
(gdb) run
Starting program: \\Mac\Home\Documents\typora\\OS-homework\14chapter/null.exe
[New Thread 4632.0x12f4]
[New Thread 4632.0x15bc]
[Inferior 1 (process 4632) exited normally]
  
 
```



#### 3．最后，对这个程序使用 valgrind 工具。我们将使用属于 valgrind 的 memcheck 工具 来分析发生的情况。输入以下命令来运行程序：valgrind --leak-check=yes null。当你运行它 时会发生什么？你能解释工具的输出吗？

```shell
[root@bdkoblntuft9zca6 chapter14]# valgrind --leak-check=yes ./null
==31755== Memcheck, a memory error detector
==31755== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==31755== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==31755== Command: ./null
==31755== 
==31755== 
==31755== HEAP SUMMARY:
==31755==     in use at exit: 0 bytes in 0 blocks
==31755==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==31755== 
==31755== All heap blocks were freed -- no leaks are possible
==31755== 
==31755== For lists of detected and suppressed errors, rerun with: -s
==31755== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

```



####  4．编写一个使用 malloc()来分配内存的简单程序，但在退出之前忘记释放它。这个程 序运行时会发生什么？你可以用 gdb 来查找它的任何问题吗？用 valgrind 那（再次使用 --leak-check=yes 标志）？

```shell
[root@bdkoblntuft9zca6 chapter14]# gdb ./null2
GNU gdb (GDB) Red Hat Enterprise Linux 7.6.1-120.el7
Copyright (C) 2013 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-redhat-linux-gnu".
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>...
Reading symbols from /root/OS-work/chapter14/null2...done.
(gdb) run
Starting program: /root/OS-work/chapter14/./null2 
[Inferior 1 (process 31787) exited normally]
Missing separate debuginfos, use: debuginfo-install glibc-2.17-326.el7_9.x86_64

```



```shell
[root@bdkoblntuft9zca6 chapter14]# valgrind --leak-check=yes ./null2
==31795== Memcheck, a memory error detector
==31795== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==31795== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==31795== Command: ./null2
==31795== 
==31795== 
==31795== HEAP SUMMARY:
==31795==     in use at exit: 2 bytes in 1 blocks
==31795==   total heap usage: 1 allocs, 0 frees, 2 bytes allocated
==31795== 
==31795== 2 bytes in 1 blocks are definitely lost in loss record 1 of 1
==31795==    at 0x4C29F73: malloc (vg_replace_malloc.c:309)
==31795==    by 0x40053E: main (null2.c:5)
==31795== 
==31795== LEAK SUMMARY:
==31795==    definitely lost: 2 bytes in 1 blocks
==31795==    indirectly lost: 0 bytes in 0 blocks
==31795==      possibly lost: 0 bytes in 0 blocks
==31795==    still reachable: 0 bytes in 0 blocks
==31795==         suppressed: 0 bytes in 0 blocks
==31795== 
==31795== For lists of detected and suppressed errors, rerun with: -s
==31795== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)

```



####  5．编写一个程序，使用 malloc 创建一个名为 data、大小为 100 的整数数组。然后，将 data[100]设置为 0。当你运行这个程序时会发生什么？当你使用 valgrind 运行这个程序时会 发生什么？程序是否正确？ 

程序正常结束，没有错误；

```c
#include <stdlib.h>
#include <stdio.h>
int main() {
    int data[100] = {0};
    printf("data 10 = %d",data[0]);
    return 0;
}
```



```shell
[root@bdkoblntuft9zca6 chapter14]# valgrind ./data
==31885== Memcheck, a memory error detector
==31885== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==31885== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==31885== Command: ./data
==31885== 
==31885== 
==31885== HEAP SUMMARY:
==31885==     in use at exit: 0 bytes in 0 blocks
==31885==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==31885== 
==31885== All heap blocks were freed -- no leaks are possible
==31885== 
==31885== For lists of detected and suppressed errors, rerun with: -s
==31885== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)

```



#### 6．创建一个分配整数数组的程序（如上所述），释放它们，然后尝试打印数组中某个 元素的值。程序会运行吗？当你使用 valgrind 时会发生什么？ 

系统声明的空间，无法手动释放

```c
#include <stdlib.h>
#include <stdio.h>
int main() {
    int data[100] = {0};
    free(data);
    printf("data 10 = %d",data[0]);
    return 0;
}
```



```shell
[root@bdkoblntuft9zca6 chapter14]# valgrind ./freeData
==31950== Memcheck, a memory error detector
==31950== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==31950== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==31950== Command: ./freeData
==31950== 
==31950== Invalid free() / delete / delete[] / realloc()
==31950==    at 0x4C2B06D: free (vg_replace_malloc.c:540)
==31950==    by 0x4005B0: main (in /root/OS-work/chapter14/freeData)
==31950==  Address 0x1fff000330 is on thread 1's stack
==31950==  in frame #1, created by main (???:)
==31950== 
data 10 = 0==31950== 
==31950== HEAP SUMMARY:
==31950==     in use at exit: 0 bytes in 0 blocks
==31950==   total heap usage: 0 allocs, 1 frees, 0 bytes allocated
==31950== 
==31950== All heap blocks were freed -- no leaks are possible
==31950== 
==31950== For lists of detected and suppressed errors, rerun with: -s
==31950== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)

```



#### 7．现在传递一个有趣的值来释放（例如，在上面分配的数组中间的一个指针）。会发生 什么？你是否需要工具来找到这种类型的问题？

和释放数组报错一样的

```c
#include <stdlib.h>
#include <stdio.h>
int main() {
    int data[100] = {0};
    free(&data[1]);
    printf("data 10 = %p\n",&data[0]);
    printf("data 10 = %p\n",&data[1]);
    printf("data 10 = %p\n",&data[2]);
    return 0;
}
```



```shell
[root@bdkoblntuft9zca6 chapter14]# valgrind ./freePointer
==32005== Memcheck, a memory error detector
==32005== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==32005== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==32005== Command: ./freePointer
==32005== 
==32005== Invalid free() / delete / delete[] / realloc()
==32005==    at 0x4C2B06D: free (vg_replace_malloc.c:540)
==32005==    by 0x4005B4: main (in /root/OS-work/chapter14/freePointer)
==32005==  Address 0x1fff000334 is on thread 1's stack
==32005==  in frame #1, created by main (???:)
==32005== 
data 10 = 0x1fff000330
data 10 = 0x1fff000334
data 10 = 0x1fff000338
==32005== 
==32005== HEAP SUMMARY:
==32005==     in use at exit: 0 bytes in 0 blocks
==32005==   total heap usage: 0 allocs, 1 frees, 0 bytes allocated
==32005== 
==32005== All heap blocks were freed -- no leaks are possible
==32005== 
==32005== For lists of detected and suppressed errors, rerun with: -s
==32005== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)

```



#### 8．尝试一些其他接口来分配内存。例如，创建一个简单的向量似的数据结构，以及使 用 realloc()来管理向量的相关函数。使用数组来存储向量元素。当用户在向量中添加条目时， 请使用realloc()为其分配本多空间。这样的向量表现如何？它与链表相比如何？使用valgrind 来帮助你发现错误。 





#### 9．花更多时间阅读有关使用 gdb 和 valgrind 的信息。了解你的工具至关重要，花时间 学习如何成为 UNIX 和 C 环境中的调试器专家。