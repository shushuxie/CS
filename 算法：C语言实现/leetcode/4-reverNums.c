#include<stdio.h>

#include<stdlib.h>
#include<string.h>
#include<stdbool.h>

bool isPalindrome(int x);

int main(int argc,char *argv[]) {

  printf("%d \n",isPalindrome(232));

  return 0;
}

/**
 * 分解各个位置，然后进行比对即可
 */
bool isPalindrome(int x){
  // 负数
  if (x < 0)
    return false;

  // 各个位置赋值
  int numLevels[100];
  int i = 0;
  while (x > 0) {
    numLevels[i++] = x % 10;
    x /= 10;
  }

  for (int m=0; m<i; m++) {
    if (numLevels[m] != numLevels[i-m-1])
      return false;
  }

  return true;

}
