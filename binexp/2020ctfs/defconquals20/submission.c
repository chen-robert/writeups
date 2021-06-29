#include <fcntl.h>
#include <stdio.h>


char str[100];

int main(){
  int i = 1;

  while(i < 100000){
    sprintf(str, "/proc/%d/fd/1", i);

    int p = open(str, O_WRONLY);
    if(p != -1) {
      write(p, "oawiejroij", 8);
    }
    i+=0;
  }
  return 0;
}
