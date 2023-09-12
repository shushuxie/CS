#### 1．首先用标志-p flag.s 运行 x86.py。该代码通过一个内存标志“实现”锁。你能理解 汇编代码试图做什么吗？

```assembly
  cat flag.s
.var flag
.var count

.main
.top

.acquire
mov  flag, %ax      # get flag
test $0, %ax        # if we get 0 back: lock is free!
jne  .acquire       # if not, try again
mov  $1, flag       # store 1 into flag
; 上面的代码时实现循环获取锁，如果没有获取锁说明被别的线程占领，然后循环直到释放，自己占有，设置值为1；
# critical section
mov  count, %ax     # get the value at the address
add  $1, %ax        # increment it
mov  %ax, count     # store it back

# release lock
mov  $0, flag       # clear the flag now

# see if we're still looping
sub  $1, %bx
test $0, %bx
jgt .top

halt
```



####  2．使用默认值运行时，flag.s 是否按预期工作？ 它会产生正确的结果吗？使用-M 和-R 标志跟踪变量和寄存器（并打开-c 查看它们的 值）。你能预测代码运行时标志最终会变成什么值吗？

```assembly
  python3 x86.py -p flag.s -M 2000 -R ax -c
ARG seed 0
ARG numthreads 2
ARG program flag.s
ARG interrupt frequency 50
ARG interrupt randomness False
ARG procsched
ARG argv
ARG load address 1000
ARG memsize 128
ARG memtrace 2000
ARG regtrace ax
ARG cctrace False
ARG printstats False
ARG verbose False


 2000      ax          Thread 0                Thread 1

    0       0
    0       0   1000 mov  flag, %ax
    0       0   1001 test $0, %ax
    0       0   1002 jne  .acquire
    0       0   1003 mov  $1, flag
    0       0   1004 mov  count, %ax
    0       1   1005 add  $1, %ax
    0       1   1006 mov  %ax, count
    0       1   1007 mov  $0, flag
    0       1   1008 sub  $1, %bx
    0       1   1009 test $0, %bx
    0       1   1010 jgt .top
    0       1   1011 halt
    0       0   ----- Halt;Switch -----  ----- Halt;Switch -----
    0       0                            1000 mov  flag, %ax
    0       0                            1001 test $0, %ax
    0       0                            1002 jne  .acquire
    0       0                            1003 mov  $1, flag
    0       1                            1004 mov  count, %ax
    0       2                            1005 add  $1, %ax
    0       2                            1006 mov  %ax, count
    0       2                            1007 mov  $0, flag
    0       2                            1008 sub  $1, %bx
    0       2                            1009 test $0, %bx
    0       2                            1010 jgt .top
    0       2                            1011 halt
```



####  3．使用-a 标志更改寄存器%bx 的值（例如，如果只运行两个线程，就用-a bx = 2，bx =  2）。代码是做什么的？对这段代码问上面的问题，答案如何？

bx是循环次数

```assembly
  python3 x86.py -p flag.s -M 2000 -R ax,bx -a bx=2,bx=2 -c
ARG seed 0
ARG numthreads 2
ARG program flag.s
ARG interrupt frequency 50
ARG interrupt randomness False
ARG procsched
ARG argv bx=2,bx=2
ARG load address 1000
ARG memsize 128
ARG memtrace 2000
ARG regtrace ax,bx
ARG cctrace False
ARG printstats False
ARG verbose False


 2000      ax    bx          Thread 0                Thread 1

    0       0     2
    0       0     2   1000 mov  flag, %ax
    0       0     2   1001 test $0, %ax
    0       0     2   1002 jne  .acquire
    0       0     2   1003 mov  $1, flag
    0       0     2   1004 mov  count, %ax
    0       1     2   1005 add  $1, %ax
    0       1     2   1006 mov  %ax, count
    0       1     2   1007 mov  $0, flag
    0       1     1   1008 sub  $1, %bx
    0       1     1   1009 test $0, %bx
    0       1     1   1010 jgt .top
    0       0     1   1000 mov  flag, %ax
    0       0     1   1001 test $0, %ax
    0       0     1   1002 jne  .acquire
    0       0     1   1003 mov  $1, flag
    0       1     1   1004 mov  count, %ax
    0       2     1   1005 add  $1, %ax
    0       2     1   1006 mov  %ax, count
    0       2     1   1007 mov  $0, flag
    0       2     0   1008 sub  $1, %bx
    0       2     0   1009 test $0, %bx
    0       2     0   1010 jgt .top
    0       2     0   1011 halt
    0       0     2   ----- Halt;Switch -----  ----- Halt;Switch -----
    0       0     2                            1000 mov  flag, %ax
    0       0     2                            1001 test $0, %ax
    0       0     2                            1002 jne  .acquire
    0       0     2                            1003 mov  $1, flag
    0       2     2                            1004 mov  count, %ax
    0       3     2                            1005 add  $1, %ax
    0       3     2                            1006 mov  %ax, count
    0       3     2                            1007 mov  $0, flag
    0       3     1                            1008 sub  $1, %bx
    0       3     1                            1009 test $0, %bx
    0       3     1                            1010 jgt .top
    0       0     1                            1000 mov  flag, %ax
    0       0     1                            1001 test $0, %ax
    0       0     1                            1002 jne  .acquire
    0       0     1                            1003 mov  $1, flag
    0       3     1                            1004 mov  count, %ax
    0       4     1                            1005 add  $1, %ax
    0       4     1                            1006 mov  %ax, count
    0       4     1                            1007 mov  $0, flag
    0       4     0                            1008 sub  $1, %bx
    0       4     0                            1009 test $0, %bx
    0       4     0                            1010 jgt .top
    0       4     0                            1011 halt
```



####  4．对每个线程将 bx 设置为高值，然后使用-i 标志生成不同的中断频率。什么值导致产 生不好的结果？什么值导致产生良好的结果？ 

i = 5*x + 6会产生好的结果，1，2，3，4都不行



```shell
 python3 x86.py -p flag.s -M 2000 -R ax,bx -a bx=2,bx=2 -c -i 1
ARG seed 0
ARG numthreads 2
ARG program flag.s
ARG interrupt frequency 1
ARG interrupt randomness False
ARG procsched
ARG argv bx=2,bx=2
ARG load address 1000
ARG memsize 128
ARG memtrace 2000
ARG regtrace ax,bx
ARG cctrace False
ARG printstats False
ARG verbose False


 2000      ax    bx          Thread 0                Thread 1

    0       0     2
    0       0     2   1000 mov  flag, %ax
    0       0     2   ------ Interrupt ------  ------ Interrupt ------
    0       0     2                            1000 mov  flag, %ax
    0       0     2   ------ Interrupt ------  ------ Interrupt ------
    0       0     2   1001 test $0, %ax
    0       0     2   ------ Interrupt ------  ------ Interrupt ------
    0       0     2                            1001 test $0, %ax
    0       0     2   ------ Interrupt ------  ------ Interrupt ------
    0       0     2   1002 jne  .acquire
    0       0     2   ------ Interrupt ------  ------ Interrupt ------
    0       0     2                            1002 jne  .acquire
    0       0     2   ------ Interrupt ------  ------ Interrupt ------
    0       0     2   1003 mov  $1, flag
    0       0     2   ------ Interrupt ------  ------ Interrupt ------
    0       0     2                            1003 mov  $1, flag
    0       0     2   ------ Interrupt ------  ------ Interrupt ------
    0       0     2   1004 mov  count, %ax
    0       0     2   ------ Interrupt ------  ------ Interrupt ------
    0       0     2                            1004 mov  count, %ax
    0       0     2   ------ Interrupt ------  ------ Interrupt ------
    0       1     2   1005 add  $1, %ax
    0       0     2   ------ Interrupt ------  ------ Interrupt ------
    0       1     2                            1005 add  $1, %ax
    0       1     2   ------ Interrupt ------  ------ Interrupt ------
    0       1     2   1006 mov  %ax, count
    0       1     2   ------ Interrupt ------  ------ Interrupt ------
    0       1     2                            1006 mov  %ax, count
    0       1     2   ------ Interrupt ------  ------ Interrupt ------
    0       1     2   1007 mov  $0, flag
    0       1     2   ------ Interrupt ------  ------ Interrupt ------
    0       1     2                            1007 mov  $0, flag
    0       1     2   ------ Interrupt ------  ------ Interrupt ------
    0       1     1   1008 sub  $1, %bx
    0       1     2   ------ Interrupt ------  ------ Interrupt ------
    0       1     1                            1008 sub  $1, %bx
    0       1     1   ------ Interrupt ------  ------ Interrupt ------
    0       1     1   1009 test $0, %bx
    0       1     1   ------ Interrupt ------  ------ Interrupt ------
    0       1     1                            1009 test $0, %bx
    0       1     1   ------ Interrupt ------  ------ Interrupt ------
    0       1     1   1010 jgt .top
    0       1     1   ------ Interrupt ------  ------ Interrupt ------
    0       1     1                            1010 jgt .top
    0       1     1   ------ Interrupt ------  ------ Interrupt ------
    0       0     1   1000 mov  flag, %ax
    0       1     1   ------ Interrupt ------  ------ Interrupt ------
    0       0     1                            1000 mov  flag, %ax
    0       0     1   ------ Interrupt ------  ------ Interrupt ------
    0       0     1   1001 test $0, %ax
    0       0     1   ------ Interrupt ------  ------ Interrupt ------
    0       0     1                            1001 test $0, %ax
    0       0     1   ------ Interrupt ------  ------ Interrupt ------
    0       0     1   1002 jne  .acquire
    0       0     1   ------ Interrupt ------  ------ Interrupt ------
    0       0     1                            1002 jne  .acquire
    0       0     1   ------ Interrupt ------  ------ Interrupt ------
    0       0     1   1003 mov  $1, flag
    0       0     1   ------ Interrupt ------  ------ Interrupt ------
    0       0     1                            1003 mov  $1, flag
    0       0     1   ------ Interrupt ------  ------ Interrupt ------
    0       1     1   1004 mov  count, %ax
    0       0     1   ------ Interrupt ------  ------ Interrupt ------
    0       1     1                            1004 mov  count, %ax
    0       1     1   ------ Interrupt ------  ------ Interrupt ------
    0       2     1   1005 add  $1, %ax
    0       1     1   ------ Interrupt ------  ------ Interrupt ------
    0       2     1                            1005 add  $1, %ax
    0       2     1   ------ Interrupt ------  ------ Interrupt ------
    0       2     1   1006 mov  %ax, count
    0       2     1   ------ Interrupt ------  ------ Interrupt ------
    0       2     1                            1006 mov  %ax, count
    0       2     1   ------ Interrupt ------  ------ Interrupt ------
    0       2     1   1007 mov  $0, flag
    0       2     1   ------ Interrupt ------  ------ Interrupt ------
    0       2     1                            1007 mov  $0, flag
    0       2     1   ------ Interrupt ------  ------ Interrupt ------
    0       2     0   1008 sub  $1, %bx
    0       2     1   ------ Interrupt ------  ------ Interrupt ------
    0       2     0                            1008 sub  $1, %bx
    0       2     0   ------ Interrupt ------  ------ Interrupt ------
    0       2     0   1009 test $0, %bx
    0       2     0   ------ Interrupt ------  ------ Interrupt ------
    0       2     0                            1009 test $0, %bx
    0       2     0   ------ Interrupt ------  ------ Interrupt ------
    0       2     0   1010 jgt .top
    0       2     0   ------ Interrupt ------  ------ Interrupt ------
    0       2     0                            1010 jgt .top
    0       2     0   ------ Interrupt ------  ------ Interrupt ------
    0       2     0   1011 halt
    0       2     0   ----- Halt;Switch -----  ----- Halt;Switch -----
    0       2     0   ------ Interrupt ------  ------ Interrupt ------
    0       2     0                            1011 halt
```



#### 5．现在让我们看看程序 test-and-set.s。首先，尝试理解使用 xchg 指令构建简单锁原语 的代码。获取锁怎么写？释放锁如何写？

```c
// 加锁。判断锁是否被占用和重新设置原子化操作；
 void lock(lock_t *lock) {
 while (TestAndSet(&lock->flag, 1) == 1)
 ; // spin-wait (do nothing)
 }

void unlock(lock_t *lock) {
	 lock->flag = 0;
 }
```



####  6．现在运行代码，再次更改中断间隔（-i）的值，并确保循环多次。代码是否总能按 预期工作？有时会导致 CPU 使用率不高吗？如何量化呢？ 

代码可以正常工作，没有临界区竞争现象；

自旋等待的时候会导致cpu空转，等待锁释放

量化可以估算等待执行时间，正常线程执行一次且没有等待是有一个最短的步骤，拿实际的比较最优可以计算出步骤比例

越接近1代表越好；

#### 7．使用-P 标志生成锁相关代码的特定测试。例如，执行一个测试计划，在第一个线程 中获取锁，但随后尝试在第二个线程中获取锁。正确的事情发生了吗？你还应该测试什么？



####  8．现在让我们看看 peterson.s 中的代码，它实现了 Person 算法（在文中的补充栏中提到）。 研究这些代码，看看你能否理解它。 

```assembly
.acquire
mov $1, 0(%fx,%bx,4)    # flag[self] = 1
mov %cx, turn           # turn       = 1 - self

.spin1
mov 0(%fx,%cx,4), %ax   # flag[1-self]
test $1, %ax
jne .fini               # if flag[1-self] != 1, skip past loop to .fini

.spin2                  # just labeled for fun, not needed
mov turn, %ax
test %cx, %ax           # compare 'turn' and '1 - self'
je .spin1               # if turn==1-self, go back and start spin again

# fall out of spin
.fini

# do critical section now
mov count, %ax
add $1, %ax
mov %ax, count

.release
mov $0, 0(%fx,%bx,4)    # flag[self] = 0


# end case: make sure it's other's turn
mov %cx, turn           # turn       = 1 - self
halt
```



#### 9．现在用不同的-i 值运行代码。你看到了什么样的不同行为？ 



#### 10．你能控制调度（带-P 标志）来“证明”代码有效吗？你应该展示哪些不同情况？ 考虑互斥和避免死锁。



####  11．现在研究 ticket.s 中 ticket 锁的代码。它是否与本章中的代码相符？



####  12．现在运行代码，使用以下标志：-a bx=1000, bx=1000（此标志设置每个线程循环 1000 次）。看看随着时间的推移发生了什么，线程是否花了很多时间自旋等待锁？ 



#### 13．添加更多的线程，代码表现如何？ 



#### 14．现在来看 yield.s，其中我们假设 yield 指令能够使一个线程将 CPU 的控制权交给另 一个线程（实际上，这会是一个 OS 原语，但为了简化仿真，我们假设 有一个指令可以完 成任务）。找到一个场景，其中 test-and-set.s 浪费周期旋转，但 yield.s 不会。节省了多少指 令？这些节省在什么情况下会出现？



####  15．最后来看 test-and-test-and-set.s。这把锁有什么作用？与 test-and-set.s 相比，它实现 了什么样的优点？