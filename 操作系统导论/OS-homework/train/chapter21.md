#### 1．使用以下参数生成随机地址：-s 0 -n 10，-s 1 -n 10 和-s 2 -n 10。将策略从 FIFO 更改为 LRU，并将其更改为 OPT。
计算所述地址追踪中的每个访问是否命中或未命中。

```
$ ./paging-policy.py -s 0 -n 10
ARG addresses -1
ARG addressfile
ARG numaddrs 10
ARG policy FIFO
ARG clockbits 2
ARG cachesize 3
ARG maxpage 10
ARG seed 0
ARG notrace False

Assuming a replacement policy of FIFO, and a cache of size 3 pages,
figure out whether each of the following page references hit or miss
in the page cache.
Policy FIFO

Access: 8  Miss  [8]       [Misses:1]    
Access: 7  Miss [7,8]      [Misses:2]    
Access: 4  Miss [4,7,8]    [Misses:3]
Access: 2  Miss [2,4,7]    [Misses:4]
Access: 5  Miss [5,2,4]    [MIsses:5]
Access: 4  hit  [5,2,4]    [Misses:5]
Access: 7  Miss [7,5,2]    [Misses:6]
Access: 3  Miss [3,7,5]    [Misses:7]
Access: 4  Miss [4,3,7]    [Misses:8]
Access: 5  Miss [5,4,3]    [Misses:9]
整体命中率：10%；
缓存充满后命中率：14.3%
================================================================
Policy LRU 左侧是最少访问，右侧最多最新访问

Access: 8  Miss  [8]       [Misses:1]
Access: 7  Miss [8,7]      [Misses:2]
Access: 4  Miss [8,7,4]    [Misses:3]
Access: 2  Miss [7,4,2]    [Misses:4]
Access: 5  Miss [4,2,5]    [Misses:5]
Access: 4  hit  [2,5,4]    [Misses:5]
Access: 7  Miss [5,4,7]    [Misses:6]
Access: 3  Miss [4,7,3]    [Misses:7]
Access: 4  hit  [7,3,4]    [Misses:7]
Access: 5  Miss [3,4,5]    [Misses:8]
整体命中率： 20%
缓存充满后命中率：28.6%
==================================================================
policy OPT

Access: 8  Miss  [8]       [Misses:1]
Access: 7  Miss [8,7]      [Misses:2]
Access: 4  Miss [8,7,4]    [Misses:3]
Access: 2  Miss [7,4,2]    [Misses:4]
Access: 5  Miss [7,4,5]    [Misses:5]
Access: 4  Hit  [7,4,5]    [Misses：5]
Access: 7  Hit  [7,4,5]    [Misses:5]
Access: 3  Miss [3,4,5]    [Misses:6]
Access: 4  Hit  [3,4,5]    [Misses:6]
Access: 5  Hit  [3,4,5]    [Misses:6]
整体命中率：40%
缓存充满后命中率：57.1%
```

```
$ ./paging-policy.py -s 1 -n 10  -p FIFO
ARG addresses -1
ARG addressfile
ARG numaddrs 10
ARG policy FIFO
ARG clockbits 2
ARG cachesize 3
ARG maxpage 10
ARG seed 1
ARG notrace False

Assuming a replacement policy of FIFO, and a cache of size 3 pages,
figure out whether each of the following page references hit or miss
in the page cache.
=====================================================================
policy FIFO 
Access: 1  Miss [1]     [hit:0 misses:1] 
Access: 8  Miss [8,1]   [hit:0 misses:2]
Access: 7  Miss [7,8,1] [hit:0 misses:3]
Access: 2  Miss [2,7,8] [hit:0 misses:4]
Access: 4  Miss [4,2,7] [hit:0 misses:5]
Access: 4  Hit  [4,2,7] [hit:1 misses:5]
Access: 6  Miss [6,4,2] [hit:1 misses:6]
Access: 7  Miss [7,6,4] [hit:1 misses:7]
Access: 0  Miss [0,7,6] [hit:1 misses:8]
Access: 0  hit  [0,7,6] [hit:2 misses:8]
整体命中率： 20%
=====================================================================
policy LRU 
Access: 1  Miss [1]     [hit:0 misses:1]
Access: 8  Miss [1,8]   [hit:0 misses:2]
Access: 7  Miss [1,8,7] [hit:0 misses:3]
Access: 2  Miss [8,7,2] [hit:0 misses:4]
Access: 4  Miss [7,2,4] [hit:0 misses:5]
Access: 4  Hit  [7,2,4] [hit:1 misses:5]
Access: 6  Miss [2,4,6] [hit:1 misses:6]
Access: 7  Miss [4,6,7] [hit:1 misses:7]
Access: 0  Miss [6,7,0] [hit:1 misses:8]
Access: 0  Hit  [6,7,0] [hit:2 misses:8]
整体命中率： 20%

=====================================================================
policy OPT 
Access: 1  Miss [1]     [hit:0 misses:1] 
Access: 8  Miss [8,1]   [hit:0 misses:2]
Access: 7  Miss [7,8,1] [hit:0 misses:3]
Access: 2  Miss [7,2,1] [hit:0 misses:4]
Access: 4  Miss [4,1,7] [hit:0 misses:5]
Access: 4  Hit  [4,1,7] [hit:1 misses:5]
Access: 6  Miss [6,4,7] [hit:1 misses:6]
Access: 7  Hit  [7,6,4] [hit:2 misses:6]
Access: 0  Miss [0,7,6] [hit:2 misses:7]
Access: 0  hit  [0,7,6] [hit:3 misses:7]
整体命中率： 30%
```

#### 2．对于大小为 5 的高速缓存，为以下每个策略生成最差情况的地址引用序列：FIFO、LRU 和 MRU（最差情况下的引用序列导致尽可能多的未命中）。
对于最差情况下的引用序列，需要的缓存增大多少，才能大幅提高性能，并接近 OPT？
***FIFO 可以使用循环，只要充满缓存，页大于缓存页一个即可，刚好全部错过，此种情况增加一个缓存位即可***
```
$ ./paging-policy.py -p FIFO -a 1,2,3,4,5,6,1,2,3,4,5,6 -c -C 5
ARG addresses 1,2,3,4,5,6,1,2,3,4,5,6
ARG addressfile
ARG numaddrs 10
ARG policy FIFO
ARG clockbits 2
ARG cachesize 5
ARG maxpage 10
ARG seed 0
ARG notrace False

Solving...

Access: 1  MISS FirstIn ->          [1] <- Lastin  Replaced:- [Hits:0 Misses:1]
Access: 2  MISS FirstIn ->       [1, 2] <- Lastin  Replaced:- [Hits:0 Misses:2]
Access: 3  MISS FirstIn ->    [1, 2, 3] <- Lastin  Replaced:- [Hits:0 Misses:3]
Access: 4  MISS FirstIn -> [1, 2, 3, 4] <- Lastin  Replaced:- [Hits:0 Misses:4]
Access: 5  MISS FirstIn -> [1, 2, 3, 4, 5] <- Lastin  Replaced:- [Hits:0 Misses:5]
Access: 6  MISS FirstIn -> [2, 3, 4, 5, 6] <- Lastin  Replaced:1 [Hits:0 Misses:6]
Access: 1  MISS FirstIn -> [3, 4, 5, 6, 1] <- Lastin  Replaced:2 [Hits:0 Misses:7]
Access: 2  MISS FirstIn -> [4, 5, 6, 1, 2] <- Lastin  Replaced:3 [Hits:0 Misses:8]
Access: 3  MISS FirstIn -> [5, 6, 1, 2, 3] <- Lastin  Replaced:4 [Hits:0 Misses:9]
Access: 4  MISS FirstIn -> [6, 1, 2, 3, 4] <- Lastin  Replaced:5 [Hits:0 Misses:10]
Access: 5  MISS FirstIn -> [1, 2, 3, 4, 5] <- Lastin  Replaced:6 [Hits:0 Misses:11]
Access: 6  MISS FirstIn -> [2, 3, 4, 5, 6] <- Lastin  Replaced:1 [Hits:0 Misses:12]

FINALSTATS hits 0   misses 12   hitrate 0.00
```

LRU 最近最少使用的舍弃，满足丢弃后的页重新使用即可最少命中
```
$ ./paging-policy.py -p LRU -a 1,2,3,4,5,6,1,2,3,4,5,6 -c -C 5
ARG addresses 1,2,3,4,5,6,1,2,3,4,5,6
ARG addressfile
ARG numaddrs 10
ARG policy LRU
ARG clockbits 2
ARG cachesize 5
ARG maxpage 10
ARG seed 0
ARG notrace False

Solving...

Access: 1  MISS LRU ->          [1] <- MRU Replaced:- [Hits:0 Misses:1]
Access: 2  MISS LRU ->       [1, 2] <- MRU Replaced:- [Hits:0 Misses:2]
Access: 3  MISS LRU ->    [1, 2, 3] <- MRU Replaced:- [Hits:0 Misses:3]
Access: 4  MISS LRU -> [1, 2, 3, 4] <- MRU Replaced:- [Hits:0 Misses:4]
Access: 5  MISS LRU -> [1, 2, 3, 4, 5] <- MRU Replaced:- [Hits:0 Misses:5]
Access: 6  MISS LRU -> [2, 3, 4, 5, 6] <- MRU Replaced:1 [Hits:0 Misses:6]
Access: 1  MISS LRU -> [3, 4, 5, 6, 1] <- MRU Replaced:2 [Hits:0 Misses:7]
Access: 2  MISS LRU -> [4, 5, 6, 1, 2] <- MRU Replaced:3 [Hits:0 Misses:8]
Access: 3  MISS LRU -> [5, 6, 1, 2, 3] <- MRU Replaced:4 [Hits:0 Misses:9]
Access: 4  MISS LRU -> [6, 1, 2, 3, 4] <- MRU Replaced:5 [Hits:0 Misses:10]
Access: 5  MISS LRU -> [1, 2, 3, 4, 5] <- MRU Replaced:6 [Hits:0 Misses:11]
Access: 6  MISS LRU -> [2, 3, 4, 5, 6] <- MRU Replaced:1 [Hits:0 Misses:12]

FINALSTATS hits 0   misses 12   hitrate 0.00
```

#### 3．生成一个随机追踪序列（使用 Python 或 Perl）。你预计不同的策略在这样的追踪序列上的表现如何？

#### 4．现在生成一些局部性追踪序列。如何能够产生这样的追踪序列？LRU 表现如何？RAND比 LRU 好多少？CLOCK 表现如何？CLOCK 使用不同数量的时钟位，表现如何？

#### 5．使用像 valgrind 这样的程序来测试真实应用程序并生成虚拟页面引用序列。
例如，运行valgrind --tool = lackey --trace-mem = yes ls 将为程序 ls 所做的每个指令和数据引用，输出近乎完整的引用追踪。为了使上述仿真器有用，你必须首先将每个虚拟内存引用转换为虚拟页码参考（通过屏蔽偏移量并向右移位来完成）。为了满足大部分请求，你的应用程序追踪需要多大的缓
存？随着缓存大小的增加绘制其工作集的图形。

