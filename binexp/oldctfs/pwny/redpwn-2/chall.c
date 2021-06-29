#include <stdlib.h>
#include <stdio.h> 

#define LEN 0xdeadbeef

int main() {
  puts("Nice to meet you! What's your name? ");

  char* buffer = stdin;
  int len = read(0, buffer, LEN);

  puts("Nice to meet you, \n");
  write(1, stdout, len);

  puts("Any last thoughts?");
  read(0, buffer, LEN);
  puts("Nice meeting you!");
}
