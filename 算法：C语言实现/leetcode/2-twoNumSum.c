#include<stdio.h>
#include<string.h>
#include<stdlib.h>

/**
   难度：简单
 * 两数之和
 */

int* twoSum(int* nums, int numsSize, int target, int* returnSize);

int main(int argc,char *argv[]) {

  int nums[5] = {2,4,6,9,5};
  int *returnSize = malloc(sizeof(int));
  int *resul = malloc(sizeof(int)*2);
  int *returnResul = twoSum(nums, 5, 8, returnSize);

  return 0;
}


int* twoSum(int* nums, int numsSize, int target, int* returnSize){

  for (int i=0; i<numsSize; i++)
    {
      for (int m=i+1; m<numsSize; m++)
	if (target == nums[i] + nums[m])
	  {
	    int * ret = malloc(sizeof(int) * 2);
	    // 这样也能给指针赋值
	    ret[0] = i;
	    ret[1] = m;
	    // *point 才是给指针赋值
	    *returnSize = 2;
	    return ret;
	  }
    }
  *returnSize = 0;
  return NULL;
}
