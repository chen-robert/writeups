title: Intro To Heap
---
# Intro To Heap Pwn

---
# Resources
<https://heap-exploitation.dhavalkapil.com/introduction.html>
- Very good introduction to heap

<https://github.com/shellphish/how2heap>
- Good documentation of exploits
- Recommend downloading and messing around w/ scripts

<https://fossies.org/linux/glibc/malloc/malloc.c>
- Source code for malloc
- Can be helpful when searching for errors
- Very complex though :(

---
# What is heap pwn? 
The heap is dynamically allocated memory. Unlike the stack which is static and known at runtime, the heap allows the program to request and release memory dynamically.

Memory is requested and returned through **malloc** and **free**. 
```c
// Dynamically allocate 10 bytes
char *buffer = (char *)malloc(10);

strcpy(buffer, "hello");
printf("%s\n", buffer); // prints "hello"

// Frees/unallocates the dynamic memory allocated earlier
free(buffer);
```

Note that the specific implementation of malloc and free are determined by the standard library used. That's why, many heap pwn problems will provide you with a `libc.so.6`. 

In order to load this, you can use the `LD_PRELOAD=libc.so.6` when running the program. In pwntools, this would be done with the `env=` parameter of process.
```python
p = process("./file", env={"LD_PRELOAD": "./libc.so.6"})
```
---
# Chunks 
Remember that the heap is merely a representation of memory. Glibc organizes memory into a series of chunks. 
```
struct malloc_chunk {
  INTERNAL_SIZE_T      mchunk_prev_size;  /* Size of previous chunk (if free).  */
  INTERNAL_SIZE_T      mchunk_size;       /* Size in bytes, including overhead. */
  struct malloc_chunk* fd;                /* double links -- used only if free. */
  struct malloc_chunk* bk;
  /* Only used for large blocks: pointer to next larger size.  */
  struct malloc_chunk* fd_nextsize; /* double links -- used only if free. */
  struct malloc_chunk* bk_nextsize;
};
```
where `INTERNAL_SIZE_T` is 8 (citation needed).
Note that the **fd** and **bk** pointers are only allocated if the chunk is free.
---
# Allocated Chunks
An allocated chunk looks like
```
    chunk-> +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |             Size of previous chunk, if unallocated (P clear)  |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |             Size of chunk, in bytes                     |A|M|P|
      mem-> +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |             User data starts here...                          .
            .                                                               .
            .             (malloc_usable_size() bytes)                      .
            .                                                               |
nextchunk-> +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |             (size of chunk, but used for application data)    |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |             Size of next chunk, in bytes                |A|0|1|
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
An important thing to note is that while **mem** is the pointer returned by **malloc**, this is different than the actual chunk itself.

---
# Bins
Freed chunks of similar sizes are organized into "bins", which are just [linked lists of chunks](https://www.interviewbit.com/courses/programming/topics/linked-lists/).

Fastbins are used for servicing small requests. These tend to be used for easier pwn problems. Malloc requests of size < 0x80 go to fastbins. Unlike the other bins, fastbins maintain a singly linked list. That means that only the **fd** pointer is used. 

The bins are just arrays containing a pointer to the HEAD (and TAIL if its not a fastbin) of the linked list. 
```c
typedef struct malloc_chunk *mfastbinptr;

mfastbinptr fastbinsY[]; 
```

Note that a size of a chunk is greater than the amount of memory actually avaliable to the user because of the need to store meta-data such as size. Glibc will return the smallest chunk possible for each malloc request, or create a new one if there are none left in the fastbin. 

---
# Fastbins
The fastbins look like 
```
Fastbins[idx=0, size=0x10] 0x00
Fastbins[idx=1, size=0x20] 0x00
Fastbins[idx=2, size=0x30] 0x00
Fastbins[idx=3, size=0x40] 0x00
Fastbins[idx=4, size=0x50] 0x00
Fastbins[idx=5, size=0x60] 0x00
Fastbins[idx=6, size=0x70] 0x00
```

The size is a bit misleading. The size of a fastbin denoted here is one more than the minimum sized chunk that would fit in the fastbin. 

More specifically, the `idx` of a chunk is equal to
```c
(sizeof(chunk)) / (64bitsystem? 0x10: 0x08) - 2
```

The signifiance of the index will be apparent later on.

Finally, the fastbin is LIFO. So, chunks that go in first will go out first too.

---
# First Fit
The glibc allocator will return the first chunk it finds in the appropriate bin. This is called "first fit". 

Consider the sample code.
```
// Glibc creates new chunks because the bins are empty at the start
char *a = malloc(20);     // 0xe4b010
char *b = malloc(20);     // 0xe4b030
char *c = malloc(20);     // 0xe4b050

// Recall that the bins only hold freed chunks
free(a);
// head -> a
free(b);
// head -> b -> a
free(c);
// head -> c -> b -> a

a = malloc(20);           // 0xe4b050 returned
// head -> b -> a
b = malloc(20);           // 0xe4b030 returned
// head -> a
c = malloc(20);           // 0xe4b010 returned
// head 
```

---
# Practice Problems
[pwnable.kr](https://pwnable.kr/play.php) uaf
- Intro to Use After Free vulnerability

[Picoctf 2018](https://2018game.picoctf.com/problems) Sword

Hints
- What happens when they continue to use a pointer after freeing it (UAF vulnerability)?
- Can we get glibc to return a pointer that has recently been freed (First fit)?
