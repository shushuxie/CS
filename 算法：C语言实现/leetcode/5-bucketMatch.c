#include<stdio.h>
#include<string.h>
#include<stdbool.h>

bool isvalid(char *str);


int main(int argc, char *argv[])
{


  
  return 0;
}

// 判断括号是否匹配（）{} [] 
bool isvalid(char *str) {

  int len = strlen(str);
  int i;

  // 首位不能是匹配方
  if (str[0] == ')' || str[0] == ']' || str[0] == '}') {
    return false;
  }

  if (strlen(str) % 2 != 0) {
    return false;
  }

  char array[len];
  for (i = 0; i < len; i++) {
    if (str[i] != '\0')
      array[i] = str[i];
  }




  return false;
}
