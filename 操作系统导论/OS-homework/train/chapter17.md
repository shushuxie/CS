```powershell
  -s  随机种子
  -S  申请堆的大小
  -b  基础地址
  -H HEADERSIZE, --headerSize=HEADERSIZE
                        size of the header
  -a 单元对齐，分配空间为2^N；例如：-a 4 就会 4,8,16取值分配最小的块
  						-1->no align
  -p 空闲空间寻找策略 (BEST, WORST, FIRST)
  -l ORDER, --listOrder=ORDER
                        list order (ADDRSORT, SIZESORT+, SIZESORT-, INSERT-FRONT, INSERT-BACK)
  -C, 合并空闲列表
  -n 生成的随机操作数
  -r OPSRANGE, --range=OPSRANGE
                        max alloc size
  -P OPSPALLOC, --percentAlloc=OPSPALLOC
                        percent of ops that are allocs
  -A OPSLIST, --allocList=OPSLIST
                        instead of random, list of ops (+10,-0,etc)
  -c, --compute         compute answers for me
```

##### 1．首先运行 flag -n 10 -H 0 -p BEST -s 0 来产生一些随机分配和释放。你能预测 malloc()/free()会返回什么吗？你可以在每次请求后猜测空闲列表的状态吗？随着时间的推 移，你对空闲列表有什么发现？ 

```powershell
$ ./malloc.py  -n 10 -H 0 -p BEST -s 0
seed 0
size 100
baseAddr 1000
headerSize 0
alignment -1
policy BEST
listOrder ADDRSORT
coalesce False
numOps 10
range 10
percentAlloc 50
allocList
compute False

ptr[0] = Alloc(3) returned 1000 (searched 1 element)
Free List [size 1] : [addr:1003 sz 97)

Free(ptr[0]) 
returned 0
Free List [size 2] :[addr:1000 sz 3] [addr:1003 sz 97]

ptr[1] = Alloc(5) returned 1003
Free List [size 2] : [addr:1000 sz 3] [addr:1008 sz 92]

Free(ptr[1])
returned 0
Free List [size 3] : [addr:1000 sz 3] [addr:1003 sz 5] [addr:1008 sz 92]

ptr[2] = Alloc(8) returned 1008
Free List [size 3] : [addr:1000 sz 3] [addr:1003 sz 5] [addr:1016 sz 86]

Free(ptr[2])
returned 0
Free List [size 4] :  [addr:1000 sz 3] [addr:1003 sz 5] [addr:1008 sz 8] 
											[addr:1016 sz 86]

ptr[3] = Alloc(8) returned 1008
Free List [size 3] : [addr:1000 sz 3] [addr:1003 sz 5] [addr:1016 sz 86]

Free(ptr[3])
returned 0
Free List [size 4] :  [addr:1000 sz 3] [addr:1003 sz 5] [addr:1008 sz 8] 
											[addr:1016 sz 86]

ptr[4] = Alloc(2) returned 1000
Free List [size 4] : [addr:1002 sz 1] [addr:1003 sz 5] [addr:1008 sz 8] 
										 [addr:1016 sz 86]

ptr[5] = Alloc(7) returned 1008
Free List [size 4] : [addr:1002 sz 1] [addr:1003 sz 5] [addr:1015 sz 1] 
										 [addr:1016 sz 86]
```

##### 2．使用最差匹配策略搜索空闲列表（-p WORST）时，结果有何不同？什么改变了？ 

##### WORST 导致 大空间开始寻找

```powershell
$ ./malloc.py  -n 10 -H 0 -p WORST -s 0
seed 0
size 100
baseAddr 1000
headerSize 0
alignment -1
policy WORST
listOrder ADDRSORT
coalesce False
numOps 10
range 10
percentAlloc 50
allocList
compute False

ptr[0] = Alloc(3) returned 1000 (searched 1 element)
Free List [size 1] : [addr:1003 sz 97)

Free(ptr[0]) 
returned 0
Free List [size 2] :[addr:1000 sz 3] [addr:1003 sz 97]

ptr[1] = Alloc(5) returned 1003
Free List [size 2] : [addr:1000 sz 3] [addr:1008 sz 92]

Free(ptr[1])
returned 0
Free List [size 3] : [addr:1000 sz 3] [addr:1003 sz 5] [addr:1008 sz 92]

ptr[2] = Alloc(8) returned 1008
Free List [size 3] : [addr:1000 sz 3] [addr:1003 sz 5] [addr:1016 sz 86]

Free(ptr[2])
returned 0
Free List [size 4] :  [addr:1000 sz 3] [addr:1003 sz 5] [addr:1008 sz 8] 
											[addr:1016 sz 86]

ptr[3] = Alloc(8) returned 1008
Free List [size 4] : [addr:1000 sz 3] [addr:1003 sz 5] [addr:1008 sz 8] 
										 [addr:1024 sz 76]

Free(ptr[3])
returned 0
Free List [size 5] : [addr:1000 sz 3] [addr:1003 sz 5] [addr:1008 sz 8] 
										 [addr:1016 sz 8] [addr:1024 sz 76]

ptr[4] = Alloc(2) returned 1000
Free List [size 5] : [addr:1000 sz 3] [addr:1003 sz 5] [addr:1008 sz 8] 
										 [addr:1016 sz 8] [addr:1026 sz 74]

ptr[5] = Alloc(7) returned 1008
Free List [size 5] : [addr:1000 sz 3] [addr:1003 sz 5] [addr:1008 sz 8] 
										 [addr:1016 sz 8] [addr:1033 sz 67]
```

##### 3．如果使用首次匹配（-p FIRST）会如何？使用首次匹配时，什么变快了？

首次匹配，从前往后搜索，和best策略相似；匹配块的速度变快，不会判断所有空闲空间；

#####  4．对于上述问题，列表在保持有序时，可能会影响某些策略找到空闲位置所需的时间。 使用不同的空闲列表排序（-l ADDRSORT，-l SIZESORT +，-l SIZESORT-）查看策略和列 表排序如何相互影响。 

```powershell
ADDRSORT SIZESORT + 按地址排序增加排列； BEST匹配，worst匹配不影响；first会影响
SIzeSORT- 按地址倒序排列；First 匹配会加快；效果与WORST匹配相似
```

##### 5．合并空闲列表可能非常重要。增加随机分配的数量（比如说-n 1000）。随着时间的推移， 大型分配请求会发生什么？在有和没有合并的情况下运行（即不用和采用-C 标志）。你看到了 什么结果差异？每种情况下的空闲列表有多大？在这种情况下，列表的排序是否重要？

-S 3000 -H 0 -s 0

排序和分配策略配合起来更好；

| n    | BEST size | WORST--size | -C WORST |
| ---- | --------- | ----------- | -------- |
| 100  | 20        | 46          | 7        |
| 200  | 31        | 95          | 8        |
| 300  | 33        | 137         | 11       |
| 400  | 45        | 182         | 19       |
| 500  | 46        | 230         | 23       |
| 1000 | 97        | 489         | 15       |

#####  6．将已分配百分比-P 改为高于 50，会发生什么？它接它 100 时分配会怎样？接近 0 会怎样？ 

释放的操作变少，碎片不会增加，维持很少的碎片数；

接近0也会变稳定，请求的大小刚好有合适的，如果是worst策略会增加碎片

##### 7．要生成高度碎片化的空闲空间，你可以提出怎样的具体请求？使用-A 标志创建碎片化的空闲列表，查看不同的策略和选项如何改变空闲列表的组织。

- 多释放空间操作
- WOST策略请求
- $ ./malloc.py -S 300  -n 50 -H 0 -p FIRST  -l SIZESORT-  -s 0  -c -P 1 产生26个碎片
- $ ./malloc.py -S 300  -n 50 -H 0 -p WORST   -s 0  -c -P 1 产生26个碎片