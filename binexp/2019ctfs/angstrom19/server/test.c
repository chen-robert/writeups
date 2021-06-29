#include <stdio.h>
#include <unistd.h>

int main(void) {
  char* args[] = {"/bin/sh", "-c", "echo${IFS%?}hi",  NULL};
  char* envp[] = {NULL};
  execve("/bin/sh", args, envp);
  return 1;

}
