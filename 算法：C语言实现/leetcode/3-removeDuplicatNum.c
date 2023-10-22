#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/**
 * 难度：简单
 * 移除数组中的重复数据，返回剩余长度
 */

int removeDuplicates(int* nums, int numsSize);

int main(int argc,char* argv[]) {




  return 0;
}


int removeDuplicates(int* nums, int numsSize){
  // 双指针解法，在同一个数组上面更改
  if (numsSize == 0)
    return 0;

  // 声明指针,slow新的，fast原数组
  // 都为1 刚好满足比较初始状态，还有第一位不需要更改的情况
  int fast = 1, slow = 1;
  while (fast < numsSize) {
    if (nums[fast] != nums[fast-1]) {
      nums[slow] = nums[fast];
      ++slow;
    }
    ++fast;
  }
  
  return slow;

}
