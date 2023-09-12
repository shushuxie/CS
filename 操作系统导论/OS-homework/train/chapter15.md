#### 1．用种子 1、2 和 3 运行，并计算进程生成的每个虚拟地址是处于界限内还是界限外? 如果在界限内，请计算地址转换。 

```shell
  python3 ./segmentation.py -s 1
ARG seed 1
ARG address space size 1k
ARG phys mem size 16k

Segment register information:

  Segment 0 base  (grows positive) : 0x000030e1 (decimal 12513)
  Segment 0 limit                  : 290

  Segment 1 base  (grows negative) : 0x0000122b (decimal 4651)
  Segment 1 limit                  : 472

Virtual Address Trace
  VA  0: 0x000001fb (decimal:  507) --> PA or segmentation violation?
  VA  1: 0x000001cc (decimal:  460) --> PA or segmentation violation?
  VA  2: 0x0000029b (decimal:  667) --> PA or segmentation violation?
  VA  3: 0x00000327 (decimal:  807) --> PA or segmentation violation?
  VA  4: 0x00000060 (decimal:   96) --> PA or segmentation violation?
  
  =====================================================
  分析：segment0 是堆内存 向下增加内存地址 允许虚拟地址范围是：0-290
  segment1 是Stack，地址减小，内存范围是： 1024-472 = 552 --- 1024；
  物理地址的计算方式为 物理地址= VA + base；在stack内存中 也是这样计算，又因为 space size = 1K
  根据模运算，例如：667 --》 4651+667 = 5318 -1024 = 4294；范围符合 4651- （4651-472=4179）
  
  Segment0 decimal=[12513-12803] VA =[0,290]
  Segment1 decimal=[4179,4651] VA = [552-1024];
  VA  0: 0x000001fb (decimal:  507) --> violation
  VA  1: 0x000001cc (decimal:  460) --> vilation
  VA  2: 0x0000029b (decimal:  667) --> 4651+667-1024=4294 SEG1
  VA  3: 0x00000327 (decimal:  807) --> 4651+807-1024=4434 SEG1
  VA  4: 0x00000060 (decimal:   96) --> PA 12609 SEG0
```



```c
 python3 segmentation.py -s 2
ARG seed 2
ARG address space size 1k
ARG phys mem size 16k

Segment register information:

  Segment 0 base  (grows positive) : 0x0000039e (decimal 926)
  Segment 0 limit                  : 500

  Segment 1 base  (grows negative) : 0x0000376a (decimal 14186)
  Segment 1 limit                  : 498

Virtual Address Trace
  VA  0: 0x000002f1 (decimal:  753) --> PA or segmentation violation?
  VA  1: 0x000002ad (decimal:  685) --> PA or segmentation violation?
  VA  2: 0x0000013b (decimal:  315) --> PA or segmentation violation?
  VA  3: 0x0000026c (decimal:  620) --> PA or segmentation violation?
  VA  4: 0x0000026d (decimal:  621) --> PA or segmentation violation?
  
  ========================================================
    segment0 decimal=[926,1426] VA=[0,500]
    segment1 decimal=[13688,14186] VA=[526,1024]
    
  VA  0: 0x000002f1 (decimal:  753) --> SEG1 14186+753-1024=13945
  VA  1: 0x000002ad (decimal:  685) --> SEG1 14186+685-1024=13847
  VA  2: 0x0000013b (decimal:  315) --> SEG0 926+315=1241
  VA  3: 0x0000026c (decimal:  620) --> SEG1 14186+620-1024=13782
  VA  4: 0x0000026d (decimal:  621) --> SEG1 13783
```



```c
  python3 segmentation.py -s 3
ARG seed 3
ARG address space size 1k
ARG phys mem size 16k

Segment register information:

  Segment 0 base  (grows positive) : 0x000017ad (decimal 6061)
  Segment 0 limit                  : 316

  Segment 1 base  (grows negative) : 0x00002831 (decimal 10289)
  Segment 1 limit                  : 395

Virtual Address Trace
  VA  0: 0x00000280 (decimal:  640) --> PA or segmentation violation?
  VA  1: 0x00000043 (decimal:   67) --> PA or segmentation violation?
  VA  2: 0x0000000d (decimal:   13) --> PA or segmentation violation?
  VA  3: 0x00000359 (decimal:  857) --> PA or segmentation violation?
  VA  4: 0x00000109 (decimal:  265) --> PA or segmentation violation?
    
====================================================================
   Segment0 decimal=[6061,6377] VA =[0,316] 
   Segment1 decimal=[9894,10289] VA = [629,1024]
  VA  0: 0x00000280 (decimal:  640) --> SEG1 10289+640-1024 = 9905
  VA  1: 0x00000043 (decimal:   67) --> SEG0 6061+67 = 6128
  VA  2: 0x0000000d (decimal:   13) --> SEG0 6061+13 = 6074
  VA  3: 0x00000359 (decimal:  857) --> SEG1 10289+857-1024 = 10122
  VA  4: 0x00000109 (decimal:  265) --> SEG0 6061 + 265 = 6326
```



#### 2．使用以下标志运行：-s 0 -n 10。为了确保所有生成的虚拟地址都处于边界内，要将 -l（界限寄存器）设置为什么值？ 

len0 len1 占满分配空间即可 = 512

```c
  python3 segmentation.py -s 0 -n 10 -l 512 -L 512 -c
ARG seed 0
ARG address space size 1k
ARG phys mem size 16k

Segment register information:

  Segment 0 base  (grows positive) : 0x0000360b (decimal 13835)
  Segment 0 limit                  : 512

  Segment 1 base  (grows negative) : 0x00003282 (decimal 12930)
  Segment 1 limit                  : 512

Virtual Address Trace
  VA  0: 0x000001ae (decimal:  430) --> VALID in SEG0: 0x000037b9 (decimal: 14265)
  VA  1: 0x00000109 (decimal:  265) --> VALID in SEG0: 0x00003714 (decimal: 14100)
  VA  2: 0x0000020b (decimal:  523) --> VALID in SEG1: 0x0000308d (decimal: 12429)
  VA  3: 0x0000019e (decimal:  414) --> VALID in SEG0: 0x000037a9 (decimal: 14249)
  VA  4: 0x00000322 (decimal:  802) --> VALID in SEG1: 0x000031a4 (decimal: 12708)
  VA  5: 0x00000136 (decimal:  310) --> VALID in SEG0: 0x00003741 (decimal: 14145)
  VA  6: 0x000001e8 (decimal:  488) --> VALID in SEG0: 0x000037f3 (decimal: 14323)
  VA  7: 0x00000255 (decimal:  597) --> VALID in SEG1: 0x000030d7 (decimal: 12503)
  VA  8: 0x000003a1 (decimal:  929) --> VALID in SEG1: 0x00003223 (decimal: 12835)
  VA  9: 0x00000204 (decimal:  516) --> VALID in SEG1: 0x00003086 (decimal: 12422)
    
    === === === === ===  === === === === ===  === === === === ===  === === === === === 
    
   python3 segmentation.py -s 0 -n 10 -l 489 -L 508 -c
ARG seed 0
ARG address space size 1k
ARG phys mem size 16k

Segment register information:

  Segment 0 base  (grows positive) : 0x0000360b (decimal 13835)
  Segment 0 limit                  : 489

  Segment 1 base  (grows negative) : 0x0000327e (decimal 12926)
  Segment 1 limit                  : 508

Virtual Address Trace
  VA  0: 0x000001ae (decimal:  430) --> VALID in SEG0: 0x000037b9 (decimal: 14265)
  VA  1: 0x00000109 (decimal:  265) --> VALID in SEG0: 0x00003714 (decimal: 14100)
  VA  2: 0x0000020b (decimal:  523) --> VALID in SEG1: 0x00003089 (decimal: 12425)
  VA  3: 0x0000019e (decimal:  414) --> VALID in SEG0: 0x000037a9 (decimal: 14249)
  VA  4: 0x00000322 (decimal:  802) --> VALID in SEG1: 0x000031a0 (decimal: 12704)
  VA  5: 0x00000136 (decimal:  310) --> VALID in SEG0: 0x00003741 (decimal: 14145)
  VA  6: 0x000001e8 (decimal:  488) --> VALID in SEG0: 0x000037f3 (decimal: 14323)
  VA  7: 0x00000255 (decimal:  597) --> VALID in SEG1: 0x000030d3 (decimal: 12499)
  VA  8: 0x000003a1 (decimal:  929) --> VALID in SEG1: 0x0000321f (decimal: 12831)
  VA  9: 0x00000204 (decimal:  516) --> VALID in SEG1: 0x00003082 (decimal: 12418)
    
    不超过512 heap包含488，Stack包含516 = 1024-516 = 508
```



#### 3．使用以下标志运行：-s 1 -n 10 -l 100。可以设置界限的最大值是多少，以便地址空间 仍然完全放在物理内存中？ 



```c
  python3 segmentation.py -s 1 -n 10 -l 508 -L 357  -c
ARG seed 1
ARG address space size 1k
ARG phys mem size 16k

Segment register information:

  Segment 0 base  (grows positive) : 0x00000899 (decimal 2201)
  Segment 0 limit                  : 508

  Segment 1 base  (grows negative) : 0x000037a1 (decimal 14241)
  Segment 1 limit                  : 357

Virtual Address Trace
  VA  0: 0x0000030e (decimal:  782) --> VALID in SEG1: 0x000036af (decimal: 13999)
  VA  1: 0x00000105 (decimal:  261) --> VALID in SEG0: 0x0000099e (decimal: 2462)
  VA  2: 0x000001fb (decimal:  507) --> VALID in SEG0: 0x00000a94 (decimal: 2708)
  VA  3: 0x000001cc (decimal:  460) --> VALID in SEG0: 0x00000a65 (decimal: 2661)
  VA  4: 0x0000029b (decimal:  667) --> VALID in SEG1: 0x0000363c (decimal: 13884)
  VA  5: 0x00000327 (decimal:  807) --> VALID in SEG1: 0x000036c8 (decimal: 14024)
  VA  6: 0x00000060 (decimal:   96) --> VALID in SEG0: 0x000008f9 (decimal: 2297)
  VA  7: 0x0000001d (decimal:   29) --> VALID in SEG0: 0x000008b6 (decimal: 2230)
  VA  8: 0x00000357 (decimal:  855) --> VALID in SEG1: 0x000036f8 (decimal: 14072)
  VA  9: 0x000001bb (decimal:  443) --> VALID in SEG0: 0x00000a54 (decimal: 2644)
===============================================================================
    VA 给出的值是固定的；
    1. limit必须《=512 heap必须包含507
    2. Stack部分包含667 = 1027-667 = 357
```



#### 4．运行和第 3 题相同的操作，但使用较大的地址空间（-a）和物理内存（-p）。

```c
  python3 segmentation.py -s 1 -n 10 -l 1015  -L 714  -a 2k -p 32k -c
ARG seed 1
ARG address space size 2k
ARG phys mem size 32k

Segment register information:

  Segment 0 base  (grows positive) : 0x00001132 (decimal 4402)
  Segment 0 limit                  : 1015

  Segment 1 base  (grows negative) : 0x00006f42 (decimal 28482)
  Segment 1 limit                  : 714

Virtual Address Trace
  VA  0: 0x0000061c (decimal: 1564) --> VALID in SEG1: 0x00006d5e (decimal: 27998)
  VA  1: 0x0000020a (decimal:  522) --> VALID in SEG0: 0x0000133c (decimal: 4924)
  VA  2: 0x000003f6 (decimal: 1014) --> VALID in SEG0: 0x00001528 (decimal: 5416)
  VA  3: 0x00000398 (decimal:  920) --> VALID in SEG0: 0x000014ca (decimal: 5322)
  VA  4: 0x00000536 (decimal: 1334) --> VALID in SEG1: 0x00006c78 (decimal: 27768)
  VA  5: 0x0000064f (decimal: 1615) --> VALID in SEG1: 0x00006d91 (decimal: 28049)
  VA  6: 0x000000c0 (decimal:  192) --> VALID in SEG0: 0x000011f2 (decimal: 4594)
  VA  7: 0x0000003a (decimal:   58) --> VALID in SEG0: 0x0000116c (decimal: 4460)
  VA  8: 0x000006af (decimal: 1711) --> VALID in SEG1: 0x00006df1 (decimal: 28145)
  VA  9: 0x00000376 (decimal:  886) --> VALID in SEG0: 0x000014a8 (decimal: 5288)
    
    heap <= 1024 include 1014 must be 1015
    stack <=1024 include 1344 must be 2048-1344 = 714

```



####  5．作为边界寄存器的值的函数，随机生成的虚拟地址的哪一部分是有效的？画一个图， 使用不同随机种子运行，限制值从 0 到最大地址空间大小。

```
VA value必须 0 - limit0 或者 虚拟空间大小-limit1 -- 虚拟空间大小值 例如1k
0 -- limit0。 1024-limit1 -- 1024
limit0，limit1 小于等于分配空间的一半 1k/2；
```

