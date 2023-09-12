##### 练习

######  1．先让我们用一个小地址空间来转换一些地址。这里有一组简单的参数和几个不同的 随机种子。你可以转换这些地址吗？

 segmentation.py -a 128 -p 512 -b 0 -l 20 -B 512 -L 20 -s 0 

```powershell
$ ./segmentation.py -a 128 -p 512 -b 0 -l 20 -B 512 -L 20 -s 0
ARG seed 0
ARG address space size 128
ARG phys mem size 512

Segment register information:

  Segment 0 base  (grows positive) : 0x00000000 (decimal 0)
  Segment 0 limit                  : 20

  Segment 1 base  (grows negative) : 0x00000200 (decimal 512)
  Segment 1 limit                  : 20

Virtual Address Trace
  VA  0: 0x0000006c (decimal:  108) --> PA or segmentation violation?
  VA  1: 0x00000061 (decimal:   97) --> PA or segmentation violation?
  VA  2: 0x00000035 (decimal:   53) --> PA or segmentation violation?
  VA  3: 0x00000021 (decimal:   33) --> PA or segmentation violation?
  VA  4: 0x00000041 (decimal:   65) --> PA or segmentation violation?
  ====== ====== ====== ====== ====== ====== ====== ====== ====== ====== 
 SEG0 decimal = [0,20] VA = [0,20]
 SEG1 decimal = [492,512] VA = [108,128];
   VA  0: 0x0000006c (decimal:  108) --> SEG1 492
  VA  1: 0x00000061 (decimal:   97) -->  violation
  VA  2: 0x00000035 (decimal:   53) -->  violation
  VA  3: 0x00000021 (decimal:   33) -->  violation
  VA  4: 0x00000041 (decimal:   65) -->  violation
```

segmentation.py -a 128 -p 512 -b 0 -l 20 -B 512 -L 20 -s 1 

```powershell
$ ./segmentation.py -a 128 -p 512 -b 0 -l 20 -B 512 -L 20 -s 1
ARG seed 1
ARG address space size 128
ARG phys mem size 512

Segment register information:

  Segment 0 base  (grows positive) : 0x00000000 (decimal 0)
  Segment 0 limit                  : 20

  Segment 1 base  (grows negative) : 0x00000200 (decimal 512)
  Segment 1 limit                  : 20

Virtual Address Trace
  VA  0: 0x00000011 (decimal:   17) --> PA or segmentation violation?
  VA  1: 0x0000006c (decimal:  108) --> PA or segmentation violation?
  VA  2: 0x00000061 (decimal:   97) --> PA or segmentation violation?
  VA  3: 0x00000020 (decimal:   32) --> PA or segmentation violation?
  VA  4: 0x0000003f (decimal:   63) --> PA or segmentation violation?

====== ====== ====== ====== ====== ====== ====== ====== ====== ====== 
 SEG0 decimal = [0,20] VA = [0,20]
 SEG1 decimal = [492,512] VA = [108,128];
  VA  0: 0x00000011 (decimal:   17) --> SEG0 17
  VA  1: 0x0000006c (decimal:  108) --> SEG1 492
  VA  2: 0x00000061 (decimal:   97) --> violation
  VA  3: 0x00000020 (decimal:   32) --> violation
  VA  4: 0x0000003f (decimal:   63) --> violation
```

segmentation.py -a 128 -p 512 -b 0 -l 20 -B 512 -L 20 -s 2

```powershell
$ ./segmentation.py -a 128 -p 512 -b 0 -l 20 -B 512 -L 20 -s 2
ARG seed 2
ARG address space size 128
ARG phys mem size 512

Segment register information:

  Segment 0 base  (grows positive) : 0x00000000 (decimal 0)
  Segment 0 limit                  : 20

  Segment 1 base  (grows negative) : 0x00000200 (decimal 512)
  Segment 1 limit                  : 20

Virtual Address Trace
  VA  0: 0x0000007a (decimal:  122) --> PA or segmentation violation?
  VA  1: 0x00000079 (decimal:  121) --> PA or segmentation violation?
  VA  2: 0x00000007 (decimal:    7) --> PA or segmentation violation?
  VA  3: 0x0000000a (decimal:   10) --> PA or segmentation violation?
  VA  4: 0x0000006a (decimal:  106) --> PA or segmentation violation?

  ====== ====== ====== ====== ====== ====== ====== ====== ====== ====== 
 SEG0 decimal = [0,20] VA = [0,20]
 SEG1 decimal = [492,512] VA = [108,128];

  VA  0: 0x0000007a (decimal:  122) --> SEG1 512+122-128= 506
  VA  1: 0x00000079 (decimal:  121) --> SEG1 505
  VA  2: 0x00000007 (decimal:    7) --> SEG0 7
  VA  3: 0x0000000a (decimal:   10) --> SEG0 10
  VA  4: 0x0000006a (decimal:  106) --> violation
```



######  2．现在，让我们看看是否理解了这个构建的小地址空间（使用上面问题的参数）。段 0 中最高的合法虚拟地址是什么？段 1 中最低的合法虚拟地址是什么？在整个地址空间中， 最低和最高的非法地址是什么？最后，如何运行带有-A 标志的 segmentation.py 来测试你是 否正确？

```powershell
ARG seed 2
ARG address space size 128
ARG phys mem size 512

Segment register information:

  Segment 0 base  (grows positive) : 0x00000000 (decimal 0)
  Segment 0 limit                  : 20

  Segment 1 base  (grows negative) : 0x00000200 (decimal 512)
  Segment 1 limit                  : 20

根据生成的条件 SEG0_VA_MAX = 20 SEG1_VA_MIN= 128-20 = 108
合法VA空间为 【0,19】包含0共20个单位 【108,128】 最低非法地址20，最高非法地址 107

$ ./segmentation.py  -a 128 -p 512 -b 0 -l 20 -B 512 -L 20 -A 19,20,107,108 -c
ARG seed 0
ARG address space size 128
ARG phys mem size 512

Segment register information:

  Segment 0 base  (grows positive) : 0x00000000 (decimal 0)
  Segment 0 limit                  : 20

  Segment 1 base  (grows negative) : 0x00000200 (decimal 512)
  Segment 1 limit                  : 20

Virtual Address Trace
  VA  0: 0x00000013 (decimal:   19) --> VALID in SEG0: 0x00000013 (decimal:   19)
  VA  1: 0x00000014 (decimal:   20) --> SEGMENTATION VIOLATION (SEG0)
  VA  2: 0x0000006b (decimal:  107) --> SEGMENTATION VIOLATION (SEG1)
  VA  3: 0x0000006c (decimal:  108) --> VALID in SEG1: 0x000001ec (decimal:  492)
```

######  3．假设我们在一个 128 字节的物理内存中有一个很小的 16 字节地址空间。你会设置 什么样的基址和界限，以便让模拟器为指定的地址流生成以下转换结果：有效，有效，违 规，违反，有效，有效？假设用以下参数： segmentation.py -a 16 -p 128 -A 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 --b0 ? --l0 ? --b1 ? --l1 ? 

```powershell
  python3 segmentation.py -a 16 -p 128 -A 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 -b 5 -B 21 -l 7 -L 5 -c
ARG seed 0
ARG address space size 16
ARG phys mem size 128

Segment register information:

  Segment 0 base  (grows positive) : 0x00000005 (decimal 5)
  Segment 0 limit                  : 7

  Segment 1 base  (grows negative) : 0x00000015 (decimal 21)
  Segment 1 limit                  : 5

Virtual Address Trace
  VA  0: 0x00000000 (decimal:    0) --> VALID in SEG0: 0x00000005 (decimal:    5)
  VA  1: 0x00000001 (decimal:    1) --> VALID in SEG0: 0x00000006 (decimal:    6)
  VA  2: 0x00000002 (decimal:    2) --> VALID in SEG0: 0x00000007 (decimal:    7)
  VA  3: 0x00000003 (decimal:    3) --> VALID in SEG0: 0x00000008 (decimal:    8)
  VA  4: 0x00000004 (decimal:    4) --> VALID in SEG0: 0x00000009 (decimal:    9)
  VA  5: 0x00000005 (decimal:    5) --> VALID in SEG0: 0x0000000a (decimal:   10)
  VA  6: 0x00000006 (decimal:    6) --> VALID in SEG0: 0x0000000b (decimal:   11)
  VA  7: 0x00000007 (decimal:    7) --> SEGMENTATION VIOLATION (SEG0)
  VA  8: 0x00000008 (decimal:    8) --> SEGMENTATION VIOLATION (SEG1)
  VA  9: 0x00000009 (decimal:    9) --> SEGMENTATION VIOLATION (SEG1)
  VA 10: 0x0000000a (decimal:   10) --> SEGMENTATION VIOLATION (SEG1)
  VA 11: 0x0000000b (decimal:   11) --> VALID in SEG1: 0x00000010 (decimal:   16)
  VA 12: 0x0000000c (decimal:   12) --> VALID in SEG1: 0x00000011 (decimal:   17)
  VA 13: 0x0000000d (decimal:   13) --> VALID in SEG1: 0x00000012 (decimal:   18)
  VA 14: 0x0000000e (decimal:   14) --> VALID in SEG1: 0x00000013 (decimal:   19)
  VA 15: 0x0000000f (decimal:   15) --> VALID in SEG1: 0x00000014 (decimal:   20)

  =============== ============== ============= ============== ===================

  SEG0 decimal:[5,12] 7个单位 VA:[0,6]
  SEG1 decimal:[11,21] VA:[11,16]
```

###### 4．假设我们想要生成一个问题，其中大约 90%的随机生成的虚拟地址是有效的（即不 产生段异常）。你应该如何配置模拟器来做到这一点？哪些参数很重要？

###### 

```powershell
90%的范围合法
总分配空间为 C
(lim0 + lim1 - (C-lim1) ) / c > 9/10
10lim0 + 20lim1 > 19C
```

######  5．你可以运行模拟器，使所有虚拟地址无效吗？怎么做到？  

```powershell
  python3 segmentation.py -l 0 -L 0 -c
ARG seed 0
ARG address space size 1k
ARG phys mem size 16k

Segment register information:

  Segment 0 base  (grows positive) : 0x0000360b (decimal 13835)
  Segment 0 limit                  : 0

  Segment 1 base  (grows negative) : 0x00003082 (decimal 12418)
  Segment 1 limit                  : 0

Virtual Address Trace
  VA  0: 0x000001ae (decimal:  430) --> SEGMENTATION VIOLATION (SEG0)
  VA  1: 0x00000109 (decimal:  265) --> SEGMENTATION VIOLATION (SEG0)
  VA  2: 0x0000020b (decimal:  523) --> SEGMENTATION VIOLATION (SEG1)
  VA  3: 0x0000019e (decimal:  414) --> SEGMENTATION VIOLATION (SEG0)
  VA  4: 0x00000322 (decimal:  802) --> SEGMENTATION VIOLATION (SEG1)
```