#### 1．计算 3 个工作在随机种子为 1、2 和 3 时的模拟解。 

随机种子1

```shell
$ ./lottery.py -j 3 -s 1
ARG jlist
ARG jobs 3
ARG maxlen 10
ARG maxticket 100
ARG quantum 1
ARG seed 1

Here is the job list, with the run time of each job:
  Job 0 ( length = 1, tickets = 84 ) 0-83
  Job 1 ( length = 7, tickets = 25 ) 84-108
  Job 2 ( length = 4, tickets = 44 ) 109-153
  total tickets = 153;

Here is the set of random numbers you will need (at most):
Random 651593  mod = 119  run job2  (j2 length = 3)
Random 788724  mod = 9    run job0  (j0 length = 0)
job 0 is done at time 2
重新分配 total tickets = 69
Job 1 ( length = 7, tickets = 25 ) 0-24
Job 2 ( length = 3, tickets = 44 ) 25-69
Random 93859	mod = 19  run job 1 (j1 length = 6)
Random 28347	mod = 57  run job 2 (j2 length = 2)
Random 835765	mod = 37  run job 2 (j2 lenth = 1)
Random 432767	mod = 68  run job 2 (j2 length = 0)
job 2 is done at time 6
Job 1 ( length = 6, tickets = 25 )
Random 762280	mod = 37
Random 2106
Random 445387
Random 721540
Random 228762
Random 945271
job 1 is done at time 12

============================================================
$ ./lottery.py -j 3 -s 1 -c
ARG jlist
ARG jobs 3
ARG maxlen 10
ARG maxticket 100
ARG quantum 1
ARG seed 1

Here is the job list, with the run time of each job:
  Job 0 ( length = 1, tickets = 84 )
  Job 1 ( length = 7, tickets = 25 )
  Job 2 ( length = 4, tickets = 44 )


** Solutions **

Random 651593 -> Winning ticket 119 (of 153) -> Run 2
  Jobs:
 (  job:0 timeleft:1 tix:84 )  (  job:1 timeleft:7 tix:25 )  (* job:2 timeleft:4 tix:44 )
Random 788724 -> Winning ticket 9 (of 153) -> Run 0
  Jobs:
 (* job:0 timeleft:1 tix:84 )  (  job:1 timeleft:7 tix:25 )  (  job:2 timeleft:3 tix:44 )
--> JOB 0 DONE at time 2
Random 93859 -> Winning ticket 19 (of 69) -> Run 1
  Jobs:
 (  job:0 timeleft:0 tix:--- )  (* job:1 timeleft:7 tix:25 )  (  job:2 timeleft:3 tix:44 )
Random 28347 -> Winning ticket 57 (of 69) -> Run 2
  Jobs:
 (  job:0 timeleft:0 tix:--- )  (  job:1 timeleft:6 tix:25 )  (* job:2 timeleft:3 tix:44 )
Random 835765 -> Winning ticket 37 (of 69) -> Run 2
  Jobs:
 (  job:0 timeleft:0 tix:--- )  (  job:1 timeleft:6 tix:25 )  (* job:2 timeleft:2 tix:44 )
Random 432767 -> Winning ticket 68 (of 69) -> Run 2
  Jobs:
 (  job:0 timeleft:0 tix:--- )  (  job:1 timeleft:6 tix:25 )  (* job:2 timeleft:1 tix:44 )
--> JOB 2 DONE at time 6
Random 762280 -> Winning ticket 5 (of 25) -> Run 1
  Jobs:
 (  job:0 timeleft:0 tix:--- )  (* job:1 timeleft:6 tix:25 )  (  job:2 timeleft:0 tix:--- )
Random 2106 -> Winning ticket 6 (of 25) -> Run 1
  Jobs:
 (  job:0 timeleft:0 tix:--- )  (* job:1 timeleft:5 tix:25 )  (  job:2 timeleft:0 tix:---)
Random 445387 -> Winning ticket 12 (of 25) -> Run 1
  Jobs:
 (  job:0 timeleft:0 tix:--- )  (* job:1 timeleft:4 tix:25 )  (  job:2 timeleft:0 tix:--- )
Random 721540 -> Winning ticket 15 (of 25) -> Run 1
  Jobs:
 (  job:0 timeleft:0 tix:--- )  (* job:1 timeleft:3 tix:25 )  (  job:2 timeleft:0 tix:--- )
Random 228762 -> Winning ticket 12 (of 25) -> Run 1
  Jobs:
 (  job:0 timeleft:0 tix:--- )  (* job:1 timeleft:2 tix:25 )  (  job:2 timeleft:0 tix:--- )
Random 945271 -> Winning ticket 21 (of 25) -> Run 1
  Jobs:
 (  job:0 timeleft:0 tix:--- )  (* job:1 timeleft:1 tix:25 )  (  job:2 timeleft:0 tix:--- )
--> JOB 1 DONE at time 12

```

随机种子2

```shell
$ ./lottery.py -j 3 -s 2
ARG jlist
ARG jobs 3
ARG maxlen 10
ARG maxticket 100
ARG quantum 1
ARG seed 2

Here is the job list, with the run time of each job:
  Job 0 ( length = 9, tickets = 94 ) 0-93
  Job 1 ( length = 8, tickets = 73 ) 94-166
  Job 2 ( length = 6, tickets = 30 ) 167-196
total tickets = 197

Here is the set of random numbers you will need (at most):
Random 605944	mod = 169	run job 2 (j2 length = 5)  
Random 606802	mod = 42	run job 0 (j0 length = 8)
Random 581204	mod = 54	run job 0 (j0 length = 7)
Random 158383	mod = 192	run job 2 (j2 length = 4)
Random 430670	mod = 28	run job 0 (j0 length = 6)
Random 393532	mod = 123	run job 1 (j1 length = 7)
Random 723012	mod = 22	run job 0 (j0 length = 5)
Random 994820	mod = 167	run job 2 (j2 length = 3)
Random 949396	mod = 53	run job 0 (j0 length = 4)
Random 544177	mod = 63	run job 0 (j0 length = 3)
Random 444854	mod = 28	run job 0 (j0 length = 2)
Random 268241	mod = 124	run job 1 (j1 length = 6)
Random 35924	mod = 70	run job 0 (j0 length = 1)
Random 27444	mdo = 61	run job 0 (j0 length = 0)
job 0 is done at time 14

Job 1 ( length = 6, tickets = 73 ) 0-72
Job 2 ( length = 3, tickets = 30 ) 73-102
total tickets =  103
Random 464894	mod = 55	run job 1 (j1 length = 5)
Random 318465	mod = 92	run job 2 (j2 length = 2)
Random 380015	mod = 48	run job 1 (j1 length = 4)
Random 891790	mod = 16	run job 1 (j1 length = 3)
Random 525753	mod = 41	run job 1 (j1 length = 2)
Random 560510	mod = 87	run job 2 (j2 length = 1)
Random 236123	mod = 47	run job 1 (j1 length = 1)
Random 23858	mod = 65	run job 1 (j1 length = 0)
job 1 is done at time 22
Random 325143	mod =		run job 2 (j2 length = 0)
job 2 is done at time 23
```

随机种子3

```shell
$ ./lottery.py -j 3 -s 3
ARG jlist
ARG jobs 3
ARG maxlen 10
ARG maxticket 100
ARG quantum 1
ARG seed 3

Here is the job list, with the run time of each job:
  Job 0 ( length = 2, tickets = 54 ) 0-53
  Job 1 ( length = 3, tickets = 60 ) 54-113
  Job 2 ( length = 6, tickets = 6 ) 114-119
total tickets = 120

Here is the set of random numbers you will need (at most):
Random 13168	mod = 88	run job 1 (j1 len = 2)
Random 837469	mod = 109	run job 1 (j1 len = 1)
Random 259354	mod = 34	run job 0 (j0 len = 1)
Random 234331	mod = 91	run job 1 (j1 len = 0)
job 1 is done at time 4
Job 0 ( length = 1, tickets = 54 ) 0-53
Job 2 ( length = 6, tickets = 6 )  54-59
total tickets =  60
Random 995645	mod = 5 run job 0 (j0 len = 0)
job 0 is done at time 5
Random 470263	mod = 
Random 836462	mod = 
Random 476353	mod =
Random 639068	mod =
Random 150616	mod =
Random 634861	mod =
job 2 is done at time 11
```



#### 2．现在运行两个具体的工作：每个长度为 10，但是一个（工作 0）只有一张彩票，另 一个（工作 1）有 100 张（−l 10∶1,10∶100）。 彩票数量如此不平衡时会发生什么？在工作 1 完成之前，工作 0 是否会运行？多久？ 一般来说，这种彩票不平衡对彩票调度的行为有什么影响？

另一个几乎轮不到运行，变成了排队执行，二者差距不能过大 

```shell
$ ./lottery.py -l 10:1,10:100
ARG jlist 10:1,10:100
ARG jobs 3
ARG maxlen 10
ARG maxticket 100
ARG quantum 1
ARG seed 0

Here is the job list, with the run time of each job:
  Job 0 ( length = 10, tickets = 1 ) 0
  Job 1 ( length = 10, tickets = 100 ) 1-100
total tickets = 101

Here is the set of random numbers you will need (at most):
Random 844422	  mod = 62
Random 757955   mod = 51
Random 420572   mod = 8
Random 258917   mod = 54
Random 511275   mod = 13
Random 404934   mod = 25
Random 783799   mod = 39
Random 303313   mod = 10
Random 476597   mod = 79
Random 583382   mod = 6
job 1 is done at time 10
Random 908113   mod = 22
Random 504687   mod = 91
Random 281838   mod = 48
Random 755804   mod = 21
Random 618369   mod = 47
Random 250506   mod = 26
Random 909747   mod = 40
Random 982786   mod = 56
Random 810218   mod = 97
Random 902166   mod = 34 
job 0 is done at time 20
```



####  3．如果运行两个长度为 100 的工作，都有 100 张彩票（−l100∶100,100∶100），调度 程序有多不公平？运行一些不同的随机种子来确定（概率上的）答案。不公平性取决于一 项工作比另一项工作早完成多少。

按理说就是50%，大体上应该是公平的

```shell
s = 0
JOB 0 DONE at time 192
JOB 0 DONE at time 200
justice = 0.96
s = 1
JOB 1 DONE at time 196
JOB 0 DONE at time 200
justice = 0.98
s = 2
JOB 1 DONE at time 190
justice = 0.95
s = 3 
JOB 0 DONE at time 196
justice = 0.98

avg_justice = 0.9675
```



####  4．随着量子规模（-q）变大，你对上一个问题的答案如何改变？ 

```shell
规模变大，意味着执行的轮数变少，会变得更加不公平
python3 lottery.py -l 100:100,100:100  -s 0 -q 1 -c
JOB 0 DONE at time 192
JOB 1 DONE at time 200
justice = 0.96
python3 lottery.py -l 100:100,100:100  -s 0 -q 2 -c
--> JOB 0 DONE at time 188
justice = 0.94
python3 lottery.py -l 100:100,100:100  -s 0 -q 4 -c
JOB 1 DONE at time 176
justice = 0.88

python3 lottery.py -l 100:100,100:100  -s 0 -q 10 -c
--> JOB 1 DONE at time 150
justice = 0.75
```



#### 5．你可以制作类似本章中的图表吗？ 还有什么值得探讨的？用步长调度程序，图表看起来如何？