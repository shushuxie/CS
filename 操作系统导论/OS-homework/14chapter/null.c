#include <stdio.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>



int countLine(char *file);

int countLine(char *file) {
    int line = 0;
    int fd = open("d:/clion/OS/foo.txt",O_RDONLY);
    lseek(fd,0,SEEK_SET);
    char buf[1];
    while(read(fd,buf,1) != 0)
    {
        if (strcmp(buf,'\n') != 0)
            printf("%s",buf);
        line++;
    }
    close(fd);
    return line;
}

int
main(int argc, char *argv[])
{
//    int line = countLine("234");
//    printf("line = %d\n",line);
//    struct stat stat1;
//    stat("",&stat1);
//    char buf[20] = {'\0'};
//    int fd = open("d:/clion/OS/foo.txt",O_RDONLY);
//    int location = lseek(fd,0,SEEK_SET);
//    printf("fd = %d\n",fd);
//    printf("current location = %d\n",location);
//
//    while(read(fd,buf,1) != 0)
//    read(fd,buf,20);
//        printf("%s",buf);
//
//    close(fd);

    char *s = "hello world\n apple peach\n 1234\n 123444";
    int line = 0;
    while (*s++ == '\n')
        line ++;
    printf("line = %d",line);
    return 0;
}
