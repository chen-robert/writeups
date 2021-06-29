#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>


void handler(int signum, siginfo_t* siginfo, void* ucontext) {
    printf("siginfo: %p\n", siginfo);
    printf("code 0x%x\n", siginfo->si_code);
}

int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IONBF, 0); 

    if (argc != 2) return 0;

    int val = atoi(argv[1]);
    printf("using %d\n", val);

    struct sigaction sa = {
        .sa_flags = SA_SIGINFO,
        .sa_sigaction = handler,
    };
    sigaction(SIGTRAP, &sa, NULL);

    char* a = mmap(NULL, 0x1000, 7, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    int idx = 0;
    a[idx++] = 0x48;
    a[idx++] = 0xc7;
    a[idx++] = 0x04;
    a[idx++] = 0x24;
    a[idx++] = 0x00;
    a[idx++] = 0x01;
    a[idx++] = 0x00;
    a[idx++] = 0x00;
    a[idx++] = 0x9d;
    a[idx++] = val;
    a[idx++] = 0x0f;
    a[idx++] = 0x0b;
    
    ((void (*)()) a)();


    return 0;
}
