#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct {
char *global;
char name[0xa0];
long buffer;
long lol;
int count;
} data;

data curr;


int get_int();
void prompt();


int main() {
  curr.buffer = 0x1337;
  curr.lol = 0x420;
  
  int choice;
  int size;
  int len;
  int matches = 0;

  setvbuf(stdout, NULL, _IONBF, 0);
  
  printf("whats your name > ");
  fgets(curr.name, 0xa0, stdin);
  len = strlen(curr.name);
  if(curr.name[len - 1] == '\n') curr.name[len-1] = 0;


  printf("hi %s!\n", curr.name);

  while(1){
    prompt();
    choice = get_int();
    switch(choice){
      case 1:
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
        if(curr.count > 50){
          printf("how much paper do you want to use :/\n");
          exit(0);
        }
        
        curr.count++;
        curr.global = malloc(size);
        printf("what should i write tho > ");
        fgets(curr.global, size, stdin);
        break;
      case 2:
        if(matches >= 8){
          printf("why r u so indecisive...\n");
          exit(0);
        }
        matches++;
        printf("ok that letter was bad anyways...\n");
        free(curr.global);
        break;
      case 3:
        printf("secret name o: :");
        write(1, curr.name, 200);
        printf("\n");
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
