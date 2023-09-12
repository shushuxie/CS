#### 1．只用两个工作和两个队列运行几个随机生成的问题。针对每个工作计算 MLFQ 的执 行记录。限制每项作业的长度并关闭 I/O，让你的生活更轻松。

```shell
  python3 ./mlfq.py -j 3
Here is the list of inputs:
OPTIONS jobs 3   // 工作量 3 个
OPTIONS queues 3	// 队列 3 个
OPTIONS allotments for queue  2 is   1 //分配情况：队列2 分配job1个
OPTIONS quantum length for queue  2 is  10 // 时间片长度，队列2 是10个（每次执行）
OPTIONS allotments for queue  1 is   1 // 队列1 分配1个工作
OPTIONS quantum length for queue  1 is  10
OPTIONS allotments for queue  0 is   1 //队列 0 分配一个工作
OPTIONS quantum length for queue  0 is  10
OPTIONS boost 0    // 多久job变成高等级
OPTIONS ioTime 5		//每次IO占用5个时间片长度
OPTIONS stayAfterIO False  // io结束后不等待
OPTIONS iobump False //如果为true，则IO结束后job就到当前queue前面去等待


For each job, three defining characteristics are given:
  startTime : at what time does the job enter the system
  runTime   : the total CPU time needed by the job to finish
  ioFreq    : every ioFreq time units, the job issues an I/O
              (the I/O takes ioTime units to complete)

Job List:
  Job  0: startTime   0 - runTime  84 - ioFreq   7
  Job  1: startTime   0 - runTime  42 - ioFreq   3
  Job  2: startTime   0 - runTime  51 - ioFreq   4

Compute the execution trace for the given workloads.
If you would like, also compute the response and turnaround
times for each of the jobs.

Use the -c flag to get the exact results when you are finished.

================分析=========================================
Job List:
  Job  0: startTime   0 - runTime  84 - ioFreq   7
  Job  1: startTime   0 - runTime  42 - ioFreq   3
  Job  2: startTime   0 - runTime  51 - ioFreq   4
  
  job0在其中一个队列，占用CPU 84个时间片，io进行了7次，占用时间35个时间片

```



####  2．如何运行调度程序来重现本章中的每个实例？



####  3．将如何配置调度程序参数，像轮转调度程序那样工作？ 



#### 4．设计两个工作的负载和调度程序参数，以便一个工作利用较早的规则 4a 和 4b（用 -S 标志打开）来“愚弄”调度程序，在特定的时间间隔内获得 99%的 CPU。 



#### 5．给定一个系统，其最高队列中的时间片长度为 10ms，你需要如何频繁地将工作推回 到最高优先级级别（带有-B 标志），以保证一个长时间运行（并可能饥饿）的工作得到至少 5%的 CPU？ 



#### 6．调度中有一个问题，即刚完成 I/O 的作业添加在队列的哪一端。-I 标志改变了这个 调度模拟器的这方面行为。尝试一些工作负载，看看你是否能看到这个标志的效果。