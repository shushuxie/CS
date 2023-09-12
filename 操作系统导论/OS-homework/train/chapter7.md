



#### 1．使用 SJF 和 FIFO 调度程序运行长度为 200 的 3 个作业时，计算响应时间和周转 时间。 

两种调度都是下面的形式

| Job  | turnaroud | respnse | wait |
| ---- | --------- | ------- | :--- |
| 0    | 200       | 0       | 0    |
| 1    | 400       | 200     | 200  |
| 2    | 600       | 400     | 400  |
| AVG  | 400       | 200     | 200  |



```shell
$ python ./scheduler.py -l 200,200,200 -p FIFO -c
ARG policy FIFO
ARG jlist 200,200,200

Here is the job list, with the run time of each job:
  Job 0 ( length = 200.0 )
  Job 1 ( length = 200.0 )
  Job 2 ( length = 200.0 )


** Solutions **

Execution trace:
  [ time   0 ] Run job 0 for 200.00 secs ( DONE at 200.00 )
  [ time 200 ] Run job 1 for 200.00 secs ( DONE at 400.00 )
  [ time 400 ] Run job 2 for 200.00 secs ( DONE at 600.00 )

Final statistics:
  Job   0 -- Response: 0.00  Turnaround 200.00  Wait 0.00
  Job   1 -- Response: 200.00  Turnaround 400.00  Wait 200.00
  Job   2 -- Response: 400.00  Turnaround 600.00  Wait 400.00

  Average -- Response: 200.00  Turnaround 400.00  Wait 200.00
  
  =====================================================================
  
  $ python ./scheduler.py -l 200,200,200 -p SJF -c
ARG policy SJF
ARG jlist 200,200,200

Here is the job list, with the run time of each job:
  Job 0 ( length = 200.0 )
  Job 1 ( length = 200.0 )
  Job 2 ( length = 200.0 )


** Solutions **

Execution trace:
  [ time   0 ] Run job 0 for 200.00 secs ( DONE at 200.00 )
  [ time 200 ] Run job 1 for 200.00 secs ( DONE at 400.00 )
  [ time 400 ] Run job 2 for 200.00 secs ( DONE at 600.00 )

Final statistics:
  Job   0 -- Response: 0.00  Turnaround 200.00  Wait 0.00
  Job   1 -- Response: 200.00  Turnaround 400.00  Wait 200.00
  Job   2 -- Response: 400.00  Turnaround 600.00  Wait 400.00

  Average -- Response: 200.00  Turnaround 400.00  Wait 200.00

```



#### 2．现在做同样的事情，但有不同长度的作业，即 100、200 和 300。

#### FIFO 

| job  | turnaround | response | wait   |
| ---- | ---------- | -------- | ------ |
| 0    | 100        | 0        | 0      |
| 1    | 300        | 100      | 100    |
| 2    | 600        | 300      | 300    |
| AVG  | 333.33     | 133.33   | 133.33 |

SJF

| job  | turnaround | response | wait   |
| ---- | ---------- | -------- | ------ |
| 0    | 100        | 0        | 0      |
| 1    | 200        | 100      | 100    |
| 2    | 300        | 300      | 300    |
| AVG  | 333.33     | 133.33   | 133.33 |



```shell
$ python ./scheduler.py -l 100,200,300 -p FIFO -c
ARG policy FIFO
ARG jlist 100,200,300

Here is the job list, with the run time of each job:
  Job 0 ( length = 100.0 )
  Job 1 ( length = 200.0 )
  Job 2 ( length = 300.0 )


** Solutions **

Execution trace:
  [ time   0 ] Run job 0 for 100.00 secs ( DONE at 100.00 )
  [ time 100 ] Run job 1 for 200.00 secs ( DONE at 300.00 )
  [ time 300 ] Run job 2 for 300.00 secs ( DONE at 600.00 )

Final statistics:
  Job   0 -- Response: 0.00  Turnaround 100.00  Wait 0.00
  Job   1 -- Response: 100.00  Turnaround 300.00  Wait 100.00
  Job   2 -- Response: 300.00  Turnaround 600.00  Wait 300.00

  Average -- Response: 133.33  Turnaround 333.33  Wait 133.33


=============================================================

$ python ./scheduler.py -l 100,200,300 -p SJF -c
ARG policy SJF
ARG jlist 100,200,300

Here is the job list, with the run time of each job:
  Job 0 ( length = 100.0 )
  Job 1 ( length = 200.0 )
  Job 2 ( length = 300.0 )


** Solutions **

Execution trace:
  [ time   0 ] Run job 0 for 100.00 secs ( DONE at 100.00 )
  [ time 100 ] Run job 1 for 200.00 secs ( DONE at 300.00 )
  [ time 300 ] Run job 2 for 300.00 secs ( DONE at 600.00 )

Final statistics:
  Job   0 -- Response: 0.00  Turnaround 100.00  Wait 0.00
  Job   1 -- Response: 100.00  Turnaround 300.00  Wait 100.00
  Job   2 -- Response: 300.00  Turnaround 600.00  Wait 300.00

  Average -- Response: 133.33  Turnaround 333.33  Wait 133.33
```



#### 3．现在做同样的事情，但采用 RR 调度程序，时间片为 1。

等待时间 = 执行周期内除自己执行时间的以外时间

wait_job_0 = 在最后一次执行结束前，每执行一次就等待2sec = 199*2 = 398

wait_job_1 = 在最后一次执行结束前，每执行一次就等待2sec，开始多等待0一次 =  199*2+1 = 399

| job  | turnaround | response | wait  |
| ---- | ---------- | -------- | ----- |
| 0    | 598        | 0        | 388   |
| 1    | 599        | 1        | 399   |
| 2    | 600        | 2        | 400   |
| AVG  | `599`      | `1`      | `399` |

```sehll
$ python ./scheduler.py -l 10,10,10 -p RR -q 1 -c
ARG policy RR
ARG jlist 10,10,10

Here is the job list, with the run time of each job:
  Job 0 ( length = 10.0 )
  Job 1 ( length = 10.0 )
  Job 2 ( length = 10.0 )


** Solutions **

Execution trace:
  [ time   0 ] Run job   0 for 1.00 secs
  [ time   1 ] Run job   1 for 1.00 secs
  [ time   2 ] Run job   2 for 1.00 secs
  [ time   3 ] Run job   0 for 1.00 secs
  [ time   4 ] Run job   1 for 1.00 secs
  [ time   5 ] Run job   2 for 1.00 secs
  [ time   6 ] Run job   0 for 1.00 secs
  [ time   7 ] Run job   1 for 1.00 secs
  [ time   8 ] Run job   2 for 1.00 secs
  [ time   9 ] Run job   0 for 1.00 secs
  [ time  10 ] Run job   1 for 1.00 secs
  [ time  11 ] Run job   2 for 1.00 secs
  [ time  12 ] Run job   0 for 1.00 secs
  [ time  13 ] Run job   1 for 1.00 secs
  [ time  14 ] Run job   2 for 1.00 secs
  [ time  15 ] Run job   0 for 1.00 secs
  [ time  16 ] Run job   1 for 1.00 secs
  [ time  17 ] Run job   2 for 1.00 secs
  [ time  18 ] Run job   0 for 1.00 secs
  [ time  19 ] Run job   1 for 1.00 secs
  [ time  20 ] Run job   2 for 1.00 secs
  [ time  21 ] Run job   0 for 1.00 secs
  [ time  22 ] Run job   1 for 1.00 secs
  [ time  23 ] Run job   2 for 1.00 secs
  [ time  24 ] Run job   0 for 1.00 secs
  [ time  25 ] Run job   1 for 1.00 secs
  [ time  26 ] Run job   2 for 1.00 secs
  [ time  27 ] Run job   0 for 1.00 secs ( DONE at 28.00 )
  [ time  28 ] Run job   1 for 1.00 secs ( DONE at 29.00 )
  [ time  29 ] Run job   2 for 1.00 secs ( DONE at 30.00 )

Final statistics:
  Job   0 -- Response: 0.00  Turnaround 28.00  Wait 18.00
  Job   1 -- Response: 1.00  Turnaround 29.00  Wait 19.00
  Job   2 -- Response: 2.00  Turnaround 30.00  Wait 20.00

  Average -- Response: 1.00  Turnaround 29.00  Wait 19.00
```



####  4．对于什么类型的工作负载，SJF 提供与 FIFO 相同的周转时间？

​	分析：等时负载，或者不等时但是工作进入符合SJF顺序的

####  5．对于什么类型的工作负载和时间片长度，SJF 与 RR 提供相同的响应时间？

分析：负载需要的时长，刚好是时间片长度，切换就一样了

####  6．随着工作长度的增加，SJF 的响应时间会怎样？你能使用模拟程序来展示趋势吗？

分析：响应时间会增加，工作长度都在增加



####  7．随着量子长度的增加，RR 的响应时间会怎样？你能写出一个方程，计算给定 N 个 工作时，最坏情况的响应时间吗？

分析：增加；0 R 2R

N个工作肯定要同时到达，量子长度为R ，就是有一个工作一次也没执行，N-1执行结束才执行该工作；

响应时间是（N-1）