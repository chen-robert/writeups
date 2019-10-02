#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct {
char *global[10];
char name[0xa0];
long buffer;
long lol;
int count;
} data;

data curr;


int get_int();
void prompt();
void win();

void win() {
  system("/bin/sh");
}

int main() {
  curr.buffer = 0x1337;
  curr.lol = 0x420;
  
  int choice;
  int index;
  int size;
  int len;
  int matches = 0;

  setvbuf(stdout, NULL, _IONBF, 0);
  
  printf("whats your name > ");
  fgets(curr.name, 0xe8, stdin);
  len = strlen(curr.name);
  if(curr.name[len - 1] == '\n') curr.name[len-1] = 0;


  printf("hi %s!\n", curr.name);

  while(1){
    prompt();
    choice = get_int();
    switch(choice){
      case 1:
        printf("index?\n");
        index = get_int();
        printf("how long should it be? \n");
        size = get_int();
        if(size <= 0){
          printf("omggg haxor!1!\n");
          exit(0);
        }
        if(size > 420){
          printf("i can't write that much :/\n");
          exit(0);
        }
        if(curr.count > 0x100){
          printf("how much paper do you want to use :/\n");
          exit(0);
        }
        if(index < 0 || index >= 10) {
          exit(0);
        }
        
        curr.count++;
        curr.global[index] = malloc(size);
        if(curr.global[index] < (char*) 0x604000){
          exit(0);
        }
        printf("what should i write tho > ");
        read(STDIN_FILENO, curr.global, size);
        break;
      case 2:
        printf("index?\n");
        index = get_int();
        printf("ok that letter was bad anyways...\n");
        free(curr.global[index]);
        break;
      default:
        printf("That's not a choice! :(\n");
        exit(0);
    }
  }
}

int get_int(){
  int choice;
  char buffer [67];
  
  printf("Gimme int pls > ");
  read(0, buffer, 4);
  choice = atoi(buffer);

  return choice;
}

void prompt() {
  printf("%s! rob needs your help composing an aria \n", curr.name);
  printf("1) write something \n");
  printf("2) throw it away \n");
}
