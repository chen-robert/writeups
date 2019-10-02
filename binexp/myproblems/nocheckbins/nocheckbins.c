#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *global;
char name[200];
int get_int();
void prompt();


int main() {
  int choice;
  int size;
  int len;
  int matches = 0;

  setvbuf(stdout, NULL, _IONBF, 0);
  
  printf("whats your name > ");
  fgets(name, 200, stdin);
  len = strlen(name);
  if(name[len - 1] == '\n') name[len-1] = 0;


  printf("hi %s!\n", name);

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

        global = malloc(size);
        printf("what should i write tho > ");
        fgets(global, size, stdin);
        break;
      case 2:
        if(matches >= 8){
          printf("why r u so indecisive...\n");
          exit(0);
        }
        matches++;
        printf("ok that letter was bad anyways...\n");
        free(global);
        break;
      case 3:
        printf("secret name o: :");
        write(1, name, 200);
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
  printf("%s! rob needs your help composing an aria \n", name);
  printf("1) write something \n");
  printf("2) throw it away \n");
}
