#include <stdio.h>
#include <string.h>

/**
 * 罗马数字转为整数
 *
 */


int parse(char *s) {
    //special sense IV=4 IX=9 XL=40 XC=90
    // CD = 400, CM=900
    int result = 0,temp = 0,flag = 0;
    int len = strlen(s);

    for (int i=0; i<len; i++) {

      if (s[i]=='I' && s[i+1] != '\0') {
	if (s[i+1] == 'X') {
	  temp = 9;
	  flag = 1;
	}
	if (s[i+1] == 'V') {
	  temp = 4;
	  flag = 1;
	}
      }

      if (s[i]=='X' && i+1<len) {
	if (s[i+1] == 'L') {
	  temp = 40;
	  flag = 1;
	}
	if (s[i+1] == 'C') {
	  temp = 90;
	  flag = 1;
	}
      }
      

      if (s[i]=='C' && i+1<len) {
	if (s[i+1] == 'D') {
	  temp = 400;
	  flag = 1;
	}
	if (s[i+1] == 'M') {
	  temp = 900;
	  flag = 1;
	}
      }

      if (flag)
	i++;

      // 单个字符处理
      if (!flag)
       switch (s[i]) {
            case 'I':
                temp = 1;
                break;
            case 'V':
                temp = 5;
                break;
            case 'X':
                temp = 10;
                break;
            case 'L':
                temp = 50;
                break;
            case 'C':
                temp = 100;
                break;
            case 'D':
                temp = 500;
                break;
            case 'M':
                temp = 1000;
                break;
        }

      result += temp;

    }
    return result;
  

  
}

int
main(int argc,char *argv[]) {

  
  int result = parse(argv[1]);
  printf("%d \n", result);


  return 0;
}
