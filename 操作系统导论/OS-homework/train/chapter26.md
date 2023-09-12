111

```abap
mov immediate, register     # moves immediate value to register
mov memory, register        # loads from memory into register
mov register, register      # moves value from one register to other
mov register, memory        # stores register contents in memory
mov immediate, memory       # stores immediate value in memory

add immediate, register     # register  = register  + immediate
add register1, register2    # register2 = register2 + register1
sub immediate, register     # register  = register  - immediate
sub register1, register2    # register2 = register2 - register1

test immediate, register    # compare immediate and register (set condition codes)
test register, immediate    # same but register and immediate
test register, register     # same but register and register

jne                         # jump if test'd values are not equal
je                          #                       ... equal
jlt                         #     ... second is less than first
jlte                        #               ... less than or equal
jgt                         #            ... is greater than
jgte                        #               ... greater than or equal

xchg register, memory       # atomic exchange: 
                            #   put value of register into memory
                            #   return old contents of memory into reg
                            # do both things atomically

nop                         # no op
```

####  1．开始，我们来看一个简单的程序，“loop.s”。首先，阅读这个程序，看看你是否能理 解它：

cat loop.s。然后，用这些参数运行它： ./x86.py -p loop.s -t 1 -i 100 -R dx 

这指定了一个单线程，每 100 条指令产生一个中断，并且追踪寄存器%dx。你能弄清楚 %dx 在运行过程中的价值吗？你有答案之后，运行上面的代码并使用-c 标志来检查你的答 案。注意答案的左边显示了右侧指令运行后寄存器的值（或内存的值）。  

```abap
$ cat loop.s
.main
.top
sub  $1,%dx
test $0,%dx
jgte .top
halt


$ ./x86.py -p loop.s  -t 1 -i 100 -R dx -c
ARG seed 0
ARG numthreads 1
ARG program loop.s
ARG interrupt frequency 100
ARG interrupt randomness False
ARG argv
ARG load address 1000
ARG memsize 128
ARG memtrace
ARG regtrace dx
ARG cctrace False
ARG printstats False
ARG verbose False

   dx          Thread 0
    0
   -1   1000 sub  $1,%dx
   -1   1001 test $0,%dx
   -1   1002 jgte .top
   -1   1003 halt
```

####  2．现在运行相同的代码，但使用这些标志： ./x86.py -p loop.s -t 2 -i 100 -a dx=3,dx=3 -R dx 这指定了两个线程，并将每个%dx 寄存器初始化为 3。%dx 会看到什么值？使用-c 标志  运行以查看答案。多个线程的存在是否会影响计算？这段代码有竞态条件吗？  

%dx会显示为3，没有竞态条件，先运行完Thread0然后运行Thread1；

```abap
$  ./x86.py -p loop.s -t 2 -i 100 -a dx=3,dx=3 -R dx -c
ARG seed 0
ARG numthreads 2
ARG program loop.s
ARG interrupt frequency 100
ARG interrupt randomness False
ARG argv dx=3,dx=3
ARG load address 1000
ARG memsize 128
ARG memtrace
ARG regtrace dx
ARG cctrace False
ARG printstats False
ARG verbose False

   dx          Thread 0                Thread 1
    3
    2   1000 sub  $1,%dx
    2   1001 test $0,%dx
    2   1002 jgte .top
    1   1000 sub  $1,%dx
    1   1001 test $0,%dx
    1   1002 jgte .top
    0   1000 sub  $1,%dx
    0   1001 test $0,%dx
    0   1002 jgte .top
   -1   1000 sub  $1,%dx
   -1   1001 test $0,%dx
   -1   1002 jgte .top
   -1   1003 halt
    3   ----- Halt;Switch -----  ----- Halt;Switch -----
    2                            1000 sub  $1,%dx
    2                            1001 test $0,%dx
    2                            1002 jgte .top
    1                            1000 sub  $1,%dx
    1                            1001 test $0,%dx
    1                            1002 jgte .top
    0                            1000 sub  $1,%dx
    0                            1001 test $0,%dx
    0                            1002 jgte .top
   -1                            1000 sub  $1,%dx
   -1                            1001 test $0,%dx
   -1                            1002 jgte .top
   -1                            1003 halt
```

####  3．现在运行以下命令： ./x86.py -p loop.s -t 2 -i 3 -r -a dx=3,dx=3 -R dx 这使得中断间隔非常小且随机。使用不同的种子和-s 来查看不同的交替。中断频率是否 会改变这个程序的行为？  

```abap
$ ./x86.py -p loop.s -t 2 -i 3 -r -a dx=3,dx=3 -R dx
ARG seed 0
ARG numthreads 2
ARG program loop.s
ARG interrupt frequency 3
ARG interrupt randomness True
ARG argv dx=3,dx=3
ARG load address 1000
ARG memsize 128
ARG memtrace
ARG regtrace dx
ARG cctrace False
ARG printstats False
ARG verbose False

 dx          Thread 0                Thread 1
    3
    2   1000 sub  $1,%dx
    2   1001 test $0,%dx
    2   1002 jgte .top
    3   ------ Interrupt ------  ------ Interrupt ------
    2                            1000 sub  $1,%dx
    2                            1001 test $0,%dx
    2                            1002 jgte .top
    2   ------ Interrupt ------  ------ Interrupt ------
    1   1000 sub  $1,%dx
    1   1001 test $0,%dx
    2   ------ Interrupt ------  ------ Interrupt ------
    1                            1000 sub  $1,%dx
    1   ------ Interrupt ------  ------ Interrupt ------
    1   1002 jgte .top
    0   1000 sub  $1,%dx
    1   ------ Interrupt ------  ------ Interrupt ------
    1                            1001 test $0,%dx
    1                            1002 jgte .top
    0   ------ Interrupt ------  ------ Interrupt ------
    0   1001 test $0,%dx
    0   1002 jgte .top
   -1   1000 sub  $1,%dx
    1   ------ Interrupt ------  ------ Interrupt ------
    0                            1000 sub  $1,%dx
   -1   ------ Interrupt ------  ------ Interrupt ------
   -1   1001 test $0,%dx
   -1   1002 jgte .top
    0   ------ Interrupt ------  ------ Interrupt ------
    0                            1001 test $0,%dx
    0                            1002 jgte .top
   -1   ------ Interrupt ------  ------ Interrupt ------
   -1   1003 halt
    0   ----- Halt;Switch -----  ----- Halt;Switch -----
   -1                            1000 sub  $1,%dx
   -1                            1001 test $0,%dx
   -1   ------ Interrupt ------  ------ Interrupt ------
   -1                            1002 jgte .top
   -1                            1003 halt
```

####  4．接下来我们将研究一个不同的程序（looping-race-nolock.s）。 该程序访问位于内存地址 2000 的共享变量。简单起见，我们称这个变量为 x。使用单 线程运行它，并确保你了解它的功能，如下所示： ./x86.py -p looping-race-nolock.s -t 1 -M 2000 在整个运行过程中，x（即内存地址为 2000）的值是多少？使用-c 来检查你的答案。  

```powershell
  python3 x86.py -p looping-race-nolock.s -t 1 -M 2000 -c
ARG seed 0
ARG numthreads 1
ARG program looping-race-nolock.s
ARG interrupt frequency 50
ARG interrupt randomness False
ARG argv
ARG load address 1000
ARG memsize 128
ARG memtrace 2000
ARG regtrace
ARG cctrace False
ARG printstats False
ARG verbose False

 2000          Thread 0
    0
    0   1000 mov 2000, %ax
    0   1001 add $1, %ax
    1   1002 mov %ax, 2000
    1   1003 sub  $1, %bx
    1   1004 test $0, %bx
    1   1005 jgt .top
    1   1006 halt
```

#### 5．现在运行多个迭代和线程： ./x86.py -p looping-race-nolock.s -t 2 -a bx=3 -M 2000 你明白为什么每个线程中的代码循环 3 次吗？x 的最终值是什么？

bx=3 满足循环的判断条件，就循环三次；0 1 2 3 4 5 6

```powershell
  python3 x86.py -p looping-race-nolock.s -t 2 -a bx=3 -M 2000 -c
ARG seed 0
ARG numthreads 2
ARG program looping-race-nolock.s
ARG interrupt frequency 50
ARG interrupt randomness False
ARG argv bx=3
ARG load address 1000
ARG memsize 128
ARG memtrace 2000
ARG regtrace
ARG cctrace False
ARG printstats False
ARG verbose False

 2000          Thread 0                Thread 1
    0
    0   1000 mov 2000, %ax
    0   1001 add $1, %ax
    1   1002 mov %ax, 2000
    1   1003 sub  $1, %bx
    1   1004 test $0, %bx
    1   1005 jgt .top
    1   1000 mov 2000, %ax
    1   1001 add $1, %ax
    2   1002 mov %ax, 2000
    2   1003 sub  $1, %bx
    2   1004 test $0, %bx
    2   1005 jgt .top
    2   1000 mov 2000, %ax
    2   1001 add $1, %ax
    3   1002 mov %ax, 2000
    3   1003 sub  $1, %bx
    3   1004 test $0, %bx
    3   1005 jgt .top
    3   1006 halt
    3   ----- Halt;Switch -----  ----- Halt;Switch -----
    3                            1000 mov 2000, %ax
    3                            1001 add $1, %ax
    4                            1002 mov %ax, 2000
    4                            1003 sub  $1, %bx
    4                            1004 test $0, %bx
    4                            1005 jgt .top
    4                            1000 mov 2000, %ax
    4                            1001 add $1, %ax
    5                            1002 mov %ax, 2000
    5                            1003 sub  $1, %bx
    5                            1004 test $0, %bx
    5                            1005 jgt .top
    5                            1000 mov 2000, %ax
    5                            1001 add $1, %ax
    6                            1002 mov %ax, 2000
    6                            1003 sub  $1, %bx
    6                            1004 test $0, %bx
    6                            1005 jgt .top
    6                            1006 halt
```

####  6．现在以随机中断间隔运行： ./x86.py -p looping-race-nolock.s -t 2 -M 2000 -i 4 -r -s 0 然后改变随机种子，设置-s 1，然后-s 2 等。只看线程交替，你能说出 x 的最终值是什 么吗？中断的确切位置是否重要？在哪里发生是安全的？中断在哪里会引起麻烦？换句话 说，临界区究竟在哪里？  

  0   1000 mov 2000, %ax

​    0   1001 add $1, %ax

​    1   1002 mov %ax, 2000

使用%ax进行计算必须是原子化操作才行，分开就会导致竞态

```abap
$  ./x86.py -p looping-race-nolock.s -t 2 -M 2000 -i 4 -r -s 0 -c
ARG seed 0
ARG numthreads 2
ARG program looping-race-nolock.s
ARG interrupt frequency 4
ARG interrupt randomness True
ARG argv
ARG load address 1000
ARG memsize 128
ARG memtrace 2000
ARG regtrace
ARG cctrace False
ARG printstats False
ARG verbose False

 2000          Thread 0                Thread 1
    0
    0   1000 mov 2000, %ax
    0   1001 add $1, %ax
    1   1002 mov %ax, 2000
    1   1003 sub  $1, %bx
    1   ------ Interrupt ------  ------ Interrupt ------
    1                            1000 mov 2000, %ax
    1                            1001 add $1, %ax
    2                            1002 mov %ax, 2000
    2                            1003 sub  $1, %bx
    2   ------ Interrupt ------  ------ Interrupt ------
    2   1004 test $0, %bx
    2   1005 jgt .top
    2   ------ Interrupt ------  ------ Interrupt ------
    2                            1004 test $0, %bx
    2                            1005 jgt .top
    2   ------ Interrupt ------  ------ Interrupt ------
    2   1006 halt
    2   ----- Halt;Switch -----  ----- Halt;Switch -----
    2                            1006 halt
    =======================================================
    $  ./x86.py -p looping-race-nolock.s -t 2 -M 2000 -i 2 -r -s 0 -c
ARG seed 0
ARG numthreads 2
ARG program looping-race-nolock.s
ARG interrupt frequency 2
ARG interrupt randomness True
ARG argv
ARG load address 1000
ARG memsize 128
ARG memtrace 2000
ARG regtrace
ARG cctrace False
ARG printstats False
ARG verbose False

 2000          Thread 0                Thread 1
    0
    0   1000 mov 2000, %ax
    0   1001 add $1, %ax
    0   ------ Interrupt ------  ------ Interrupt ------
    0                            1000 mov 2000, %ax
    0                            1001 add $1, %ax
    0   ------ Interrupt ------  ------ Interrupt ------
    1   1002 mov %ax, 2000
    1   ------ Interrupt ------  ------ Interrupt ------
    1                            1002 mov %ax, 2000
    1   ------ Interrupt ------  ------ Interrupt ------
    1   1003 sub  $1, %bx
    1   1004 test $0, %bx
    1   ------ Interrupt ------  ------ Interrupt ------
    1                            1003 sub  $1, %bx
    1   ------ Interrupt ------  ------ Interrupt ------
    1   1005 jgt .top
    1   1006 halt
    1   ----- Halt;Switch -----  ----- Halt;Switch -----
    1   ------ Interrupt ------  ------ Interrupt ------
    1                            1004 test $0, %bx
    1   ------ Interrupt ------  ------ Interrupt ------
    1                            1005 jgt .top
    1   ------ Interrupt ------  ------ Interrupt ------
    1                            1006 halt

    =======================================================
$  ./x86.py -p looping-race-nolock.s -t 2 -M 2000 -i 4 -r -s 1
ARG seed 1                                                    
ARG numthreads 2                                              
ARG program looping-race-nolock.s                             
ARG interrupt frequency 4                                     
ARG interrupt randomness True                                 
ARG argv                                                      
ARG load address 1000                                         
ARG memsize 128                                               
ARG memtrace 2000                                             
ARG regtrace                                                  
ARG cctrace False                                             
ARG printstats False                                          
ARG verbose False                                             
                                                              
 2000          Thread 0                Thread 1               
    0                                                         
    0   1000 mov 2000, %ax                                    
    0   ------ Interrupt ------  ------ Interrupt ------      
    0                            1000 mov 2000, %ax           
    0                            1001 add $1, %ax             
    1                            1002 mov %ax, 2000           
    1                            1003 sub  $1, %bx            
    1   ------ Interrupt ------  ------ Interrupt ------      
    1   1001 add $1, %ax                                      
    1   1002 mov %ax, 2000                                    
    1   1003 sub  $1, %bx                                     
    1   1004 test $0, %bx                                     
    1   ------ Interrupt ------  ------ Interrupt ------      
    1                            1004 test $0, %bx            
    1                            1005 jgt .top                
    1   ------ Interrupt ------  ------ Interrupt ------      
    1   1005 jgt .top                                         
    1   1006 halt                                             
    1   ----- Halt;Switch -----  ----- Halt;Switch -----      
    1   ------ Interrupt ------  ------ Interrupt ------      
    1                            1006 halt                    
```

####  7．现在使用固定的中断间隔来进一步探索程序。 运行： ./x86.py -p looping-race-nolock.s -a bx=1 -t 2 -M 2000 -i 1 看看你能否猜测共享变量 x 的最终值是什么。当你改用-i 2，-i 3 等标志呢？对于哪个中 断间隔，程序会给出“正确的”最终答案？ 

```abap
    0   1000 mov 2000, %ax
    0   1001 add $1, %ax
    1   1002 mov %ax, 2000
    这三行要一次执行才行
```

####  8．现在为更多循环运行相同的代码（例如 set -a bx = 100）。使用-i 标志设置哪些中断 间隔会导致“正确”结果？哪些间隔会导致令人惊讶的结果？

小于2就会计算错误

```abap
$ ./x86.py -p looping-race-nolock.s -a bx=10 -t 2 -M 2000 -i 3 -c
ARG seed 0
ARG numthreads 2
ARG program looping-race-nolock.s
ARG interrupt frequency 3
ARG interrupt randomness False
ARG argv bx=10
ARG load address 1000
ARG memsize 128
ARG memtrace 2000
ARG regtrace
ARG cctrace False
ARG printstats False
ARG verbose False

 2000          Thread 0                Thread 1
    0
    0   1000 mov 2000, %ax
    0   1001 add $1, %ax
    1   1002 mov %ax, 2000
    1   ------ Interrupt ------  ------ Interrupt ------
    1                            1000 mov 2000, %ax
    1                            1001 add $1, %ax
    2                            1002 mov %ax, 2000
    2   ------ Interrupt ------  ------ Interrupt ------
    2   1003 sub  $1, %bx
    2   1004 test $0, %bx
    2   1005 jgt .top
    2   ------ Interrupt ------  ------ Interrupt ------
    2                            1003 sub  $1, %bx
    2                            1004 test $0, %bx
    2                            1005 jgt .top
    2   ------ Interrupt ------  ------ Interrupt ------
    2   1000 mov 2000, %ax
    2   1001 add $1, %ax
    3   1002 mov %ax, 2000
    3   ------ Interrupt ------  ------ Interrupt ------
    3                            1000 mov 2000, %ax
    3                            1001 add $1, %ax
    4                            1002 mov %ax, 2000
    4   ------ Interrupt ------  ------ Interrupt ------
    4   1003 sub  $1, %bx
    4   1004 test $0, %bx
    4   1005 jgt .top
    4   ------ Interrupt ------  ------ Interrupt ------
    4                            1003 sub  $1, %bx
    4                            1004 test $0, %bx
    4                            1005 jgt .top
    4   ------ Interrupt ------  ------ Interrupt ------
    4   1000 mov 2000, %ax
    4   1001 add $1, %ax
    5   1002 mov %ax, 2000
    5   ------ Interrupt ------  ------ Interrupt ------
    5                            1000 mov 2000, %ax
    5                            1001 add $1, %ax
    6                            1002 mov %ax, 2000
    6   ------ Interrupt ------  ------ Interrupt ------
    6   1003 sub  $1, %bx
    6   1004 test $0, %bx
    6   1005 jgt .top
    6   ------ Interrupt ------  ------ Interrupt ------
    6                            1003 sub  $1, %bx
    6                            1004 test $0, %bx
    6                            1005 jgt .top
    6   ------ Interrupt ------  ------ Interrupt ------
    6   1000 mov 2000, %ax
    6   1001 add $1, %ax
    7   1002 mov %ax, 2000
    7   ------ Interrupt ------  ------ Interrupt ------
    7                            1000 mov 2000, %ax
    7                            1001 add $1, %ax
    8                            1002 mov %ax, 2000
    8   ------ Interrupt ------  ------ Interrupt ------
    8   1003 sub  $1, %bx
    8   1004 test $0, %bx
    8   1005 jgt .top
    8   ------ Interrupt ------  ------ Interrupt ------
    8                            1003 sub  $1, %bx
    8                            1004 test $0, %bx
    8                            1005 jgt .top
    8   ------ Interrupt ------  ------ Interrupt ------
    8   1000 mov 2000, %ax
    8   1001 add $1, %ax
    9   1002 mov %ax, 2000
    9   ------ Interrupt ------  ------ Interrupt ------
    9                            1000 mov 2000, %ax
    9                            1001 add $1, %ax
   10                            1002 mov %ax, 2000
   10   ------ Interrupt ------  ------ Interrupt ------
   10   1003 sub  $1, %bx
   10   1004 test $0, %bx
   10   1005 jgt .top
   10   ------ Interrupt ------  ------ Interrupt ------
   10                            1003 sub  $1, %bx
   10                            1004 test $0, %bx
   10                            1005 jgt .top
   10   ------ Interrupt ------  ------ Interrupt ------
   10   1000 mov 2000, %ax
   10   1001 add $1, %ax
   11   1002 mov %ax, 2000
   11   ------ Interrupt ------  ------ Interrupt ------
   11                            1000 mov 2000, %ax
   11                            1001 add $1, %ax
   12                            1002 mov %ax, 2000
   12   ------ Interrupt ------  ------ Interrupt ------
   12   1003 sub  $1, %bx
   12   1004 test $0, %bx
   12   1005 jgt .top
   12   ------ Interrupt ------  ------ Interrupt ------
   12                            1003 sub  $1, %bx
   12                            1004 test $0, %bx
   12                            1005 jgt .top
   12   ------ Interrupt ------  ------ Interrupt ------
   12   1000 mov 2000, %ax
   12   1001 add $1, %ax
   13   1002 mov %ax, 2000
   13   ------ Interrupt ------  ------ Interrupt ------
   13                            1000 mov 2000, %ax
   13                            1001 add $1, %ax
   14                            1002 mov %ax, 2000
   14   ------ Interrupt ------  ------ Interrupt ------
   14   1003 sub  $1, %bx
   14   1004 test $0, %bx
   14   1005 jgt .top
   14   ------ Interrupt ------  ------ Interrupt ------
   14                            1003 sub  $1, %bx
   14                            1004 test $0, %bx
   14                            1005 jgt .top
   14   ------ Interrupt ------  ------ Interrupt ------
   14   1000 mov 2000, %ax
   14   1001 add $1, %ax
   15   1002 mov %ax, 2000
   15   ------ Interrupt ------  ------ Interrupt ------
   15                            1000 mov 2000, %ax
   15                            1001 add $1, %ax
   16                            1002 mov %ax, 2000
   16   ------ Interrupt ------  ------ Interrupt ------
   16   1003 sub  $1, %bx
   16   1004 test $0, %bx
   16   1005 jgt .top
   16   ------ Interrupt ------  ------ Interrupt ------
   16                            1003 sub  $1, %bx
   16                            1004 test $0, %bx
   16                            1005 jgt .top
   16   ------ Interrupt ------  ------ Interrupt ------
   16   1000 mov 2000, %ax
   16   1001 add $1, %ax
   17   1002 mov %ax, 2000
   17   ------ Interrupt ------  ------ Interrupt ------
   17                            1000 mov 2000, %ax
   17                            1001 add $1, %ax
   18                            1002 mov %ax, 2000
   18   ------ Interrupt ------  ------ Interrupt ------
   18   1003 sub  $1, %bx
   18   1004 test $0, %bx
   18   1005 jgt .top
   18   ------ Interrupt ------  ------ Interrupt ------
   18                            1003 sub  $1, %bx
   18                            1004 test $0, %bx
   18                            1005 jgt .top
   18   ------ Interrupt ------  ------ Interrupt ------
   18   1000 mov 2000, %ax
   18   1001 add $1, %ax
   19   1002 mov %ax, 2000
   19   ------ Interrupt ------  ------ Interrupt ------
   19                            1000 mov 2000, %ax
   19                            1001 add $1, %ax
   20                            1002 mov %ax, 2000
   20   ------ Interrupt ------  ------ Interrupt ------
   20   1003 sub  $1, %bx
   20   1004 test $0, %bx
   20   1005 jgt .top
   20   ------ Interrupt ------  ------ Interrupt ------
   20                            1003 sub  $1, %bx
   20                            1004 test $0, %bx
   20                            1005 jgt .top
   20   ------ Interrupt ------  ------ Interrupt ------
   20   1006 halt
   20   ----- Halt;Switch -----  ----- Halt;Switch -----
   20                            1006 halt
```

####    9．我们来看本作业中最后一个程序（wait-for-me.s）。 像这样运行代码： ./x86.py -p wait-for-me.s -a ax=1,ax=0 -R ax -M 2000 这将线程 0 的%ax 寄存器设置为 1，并将线程 1 的值设置为 0，在整个运行过程中观察 %ax 和内存位置 2000 的值。代码的行为应该如何？线程使用的 2000 位置的值如何？它的 最终值是什么？ 

```abap
$ ./x86.py -p wait-for-me.s -a ax=1,ax=0 -R ax -M 2000 -c
ARG seed 0
ARG numthreads 2
ARG program wait-for-me.s
ARG interrupt frequency 50
ARG interrupt randomness False
ARG argv ax=1,ax=0
ARG load address 1000
ARG memsize 128
ARG memtrace 2000
ARG regtrace ax
ARG cctrace False
ARG printstats False
ARG verbose False

 2000      ax          Thread 0                Thread 1
    0       1
    0       1   1000 test $1, %ax
    0       1   1001 je .signaller
    1       1   1006 mov  $1, 2000
    1       1   1007 halt
    1       0   ----- Halt;Switch -----  ----- Halt;Switch -----
    1       0                            1000 test $1, %ax
    1       0                            1001 je .signaller
    1       0                            1002 mov  2000, %cx
    1       0                            1003 test $1, %cx
    1       0                            1004 jne .waiter
    1       0                            1005 halt
```

#### 

#### 10．现在改变输入： ./x86.py -p wait-for-me.s -a ax=0,ax=1 -R ax -M 2000 线程行为如何？线程 0 在做什么？改变中断间隔（例如，-i 1000，或者可能使用随机间 隔）会如何改变追踪结果？程序是否高效地使用了 CPU？  

线程0没有充分使用CPU对结果没有影响，线程1才会；

```abap
$  ./x86.py -p wait-for-me.s -a ax=0,ax=1 -R ax -M 2000 -c
ARG seed 0
ARG numthreads 2
ARG program wait-for-me.s
ARG interrupt frequency 50
ARG interrupt randomness False
ARG argv ax=0,ax=1
ARG load address 1000
ARG memsize 128
ARG memtrace 2000
ARG regtrace ax
ARG cctrace False
ARG printstats False
ARG verbose False

 2000      ax          Thread 0                Thread 1
    0       0
    0       0   1000 test $1, %ax
    0       0   1001 je .signaller
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       0   1002 mov  2000, %cx
    0       0   1003 test $1, %cx
    0       0   1004 jne .waiter
    0       1   ------ Interrupt ------  ------ Interrupt ------
    0       1                            1000 test $1, %ax
    0       1                            1001 je .signaller
    1       1                            1006 mov  $1, 2000
    1       1                            1007 halt
    1       0   ----- Halt;Switch -----  ----- Halt;Switch -----
    1       0   1002 mov  2000, %cx
    1       0   1003 test $1, %cx
    1       0   1004 jne .waiter
    1       0   1005 halt
```

