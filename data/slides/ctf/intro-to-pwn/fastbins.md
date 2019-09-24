title: Fastbins in Depth
---

class: center, middle

<style>
.chunk table{
  width: 100%;
  margin: 0;
}
.chunk tr{
  display: flex;
}
.chunk td{
  width: 50%;
  border: 1px solid black;
  text-align: center;
  padding: 5px;
  margin: 5px 0;
}
</style>


# Fastbins
Robert Chen
---
# Fastbin Dup (into stack)
[Fastbin dup](https://github.com/shellphish/how2heap/blob/master/fastbin_dup.c)
- Get malloc to return the same fastbin chunk twice
- Requires double free
- Can leak heap pointers

[Fastbin dup into stack](https://github.com/shellphish/how2heap/blob/master/glibc_2.25/fastbin_dup_into_stack.c)
- Get malloc to return a chunk (with some limitations)
- Requires double free
- Can lead to arbitrary write (with some limitations)

---
# A = malloc(0x18)

Let's see what happens when we call 
```c
A = malloc(0x18)
memset(A, "A", 0x18)
```
Because the header takes up an additional 8 bytes, the smallest sized chunk that can hold our malloc request of 0x18 bytes is 0x8 + 0x18 = 0x20 bytes. 

Consider a diagram of the heap (on the next slide). Note that each block in the diagram below is 8 bytes. Furthermore, the heap grows up, so the bottom of the diagram consists of larger addresses.

---
# Diagram
.chunk[
| | | 
|---|---|
| NOT_USED | size (0x21) |
| data (AAAAAAAA) | data (AAAAAAAA) |
| data (AAAAAAAA) | top_chunk_size |
]

Heap consists of one chunk A, that's currently in use. Note that the last 3 bits of the size header are used as flags. Currently, only the PREV\_In\_USE bit is set (ones place bit) which signifies that the previous chunk is not free and in use. 

The fastbins are empty.

---
# B = malloc(0x18)

Let's malloc again, but fill the chunk with Bs. 

.chunk[
| | | 
|---|---|
| NOT_USED | size (0x21) |
| data (AAAAAAAA) | data (AAAAAAAA) |
| data (AAAAAAAA) | size (0x21) |
| data (BBBBBBBB) | data (BBBBBBBB) |
| data (BBBBBBBB) | top_chunk_size |
]

Heap consists of two chunks, A and B, which are both in use.

The fastbins are empty.

---
# free(A)
Let's see what happens when we free A.


.chunk[
| | | 
|---|---|
| NOT_USED | size (0x21) |
| fd (NULL = 0) | data (AAAAAAAA) |
| data (AAAAAAAA) | size (0x21) |
| data (BBBBBBBB) | data (BBBBBBBB) |
| data (BBBBBBBB) | top_chunk_size |
]

fastbinsY[0] = A

---
# Analysis
Some things to note. 

First, the PREV\_IN\_USE flag of chunk B is not unset (the size remains at 0x21). That's because this flag is only used for consolidating (combining) non-fastbin chunks. It's ignored when processing fastbins so you can safely ignore it for fastbin pwn. 

Second, the data in chunk A is not cleared. That could lead to a potential exploit if its used again without clearing it. This is mitigated through the use of `calloc` instead of `malloc`, which refers to "clear and allocate". `calloc` will zero the data before returning it, preventing such an exploit.

Finally, observe that `fastbinsY[0]` now points to chunk A. Malloc will first traverse the fastbins to check if a chunk of suitable size exists (this is called first fit), and return the first suitable one it finds. If the `fastbinsY` array is empty, only then will malloc create a new chunk from the top_chunk.

Note: `fastbinsY[0]` is responsible for storing all chunks of size 0x20. Chunks of size 0x30 go in `fastbinsY[1]`, and 0x40 `fastbinsY[2]`, so on until size 0x70 which is the maximum size for a fastbin.

---
# free(B)

We want to exploit a double free. However, when freeing a chunk, malloc will check the if the top chunk `fastbinsY` is the same as the chunk we are trying to free. That means `free(A)` would error now, because `A` is on top of the fastbinsY array.

To bypass this, we `free(B)`. 

.chunk[
| | | 
|---|---|
| NOT_USED | size (0x21) |
| fd (NULL = 0) | data (AAAAAAAA) |
| data (AAAAAAAA) | size (0x21) |
| fd (\*A - 0x10) | data (BBBBBBBB) |
| data (BBBBBBBB) | top_chunk_size |
]

---
# Analysis
Some things to note. 

Observe that the fd pointer of chunk B points to the address of A. That's because on free, the address of the freed chunk is written to `fastbinsY`, and the address currently stored in `fastbinsY` is stored in the `fd` pointer of the freed chunk. When we freed A, the `fd` pointer was NULL because the `fastbinsY` had nothing stored in it at that moment. 

Another oddity is that the address stored in `fd` is the address of the chunk, not the malloced data itself. The header of each chunk is 0x10 (it overlaps the PREV_SIZE or the last 8 bytes of the previous chunk), so we subtract 0x10 bytes from the pointer A. However, the addresses stored in `fastbinsY` are addresses to the malloced data (just something interesting to note). 

Now, 
```c
fastbinsY[0] = B
```

---
# free(A) ???
To finish our Fastbin Dup exploit, we `free(A)` again. 

Now our heap looks like this. 
.chunk[
| | | 
|---|---|
| NOT_USED | size (0x21) |
| fd (\*B) | data (AAAAAAAA) |
| data (AAAAAAAA) | size (0x21) |
| fd (\*A) | data (BBBBBBBB) |
| data (BBBBBBBB) | top_chunk_size |
]
```c
fastbinsY[0] = A
```
---
# Fastbin Duplicate
Note that the fastbins now form a circular array. 
A -> B -> A -> B -> A -> ...

Because of the first-principle, malloc will return the top of the fastbin array (A) first.
```c
C = malloc(0x18) // == A
D = malloc(0x18) // == B
```
Now our heap looks like this. 
.chunk[
| | | 
|---|---|
| NOT_USED | size (0x21) |
| fd / data (CCCCCCCC) | data (CCCCCCCC) |
| data (CCCCCCCC) | size (0x21) |
| data (DDDDDDDD) | data (DDDDDDDD) |
| data (DDDDDDDD) | top_chunk_size |
]

fastbinsY[0] = A

---
# Fastbin Duplicate Continued
Note that if we `malloc(0x18)` again at this point, we would get A again, resulting in the "duplicate" chunk and finishing our exploit. 

However, considering the previous diagram, note that malloc still thinks A is a free chunk. This means that it will look at the first 8 bytes or where the `fd` pointer is supposed to be, and store that in `fastbinsY[0]`. 

After `E = malloc(0x18)`, `fastbinsY[0] = 0x4343434343434343 // (CCCCCCCC)`

Note that we control this value, as we have access to chunk C which wrote this data in the first place. What if we replaced it with a fake pointer? We could write a fake value into `fastbinsY` and get malloc to return a pointer to something valuable, and then manipulate that data ourselves (e.g. the GOT table).

---
# Fastbin Duplicate into Stack
However, there are some caveats to overwriting the `fastbinsY` entry and pointing to a fake chunk. 

The fake chunk must have a valid header. Let's call our address FC (for fake chunk). The size header is located in (FC+0x8), so the 8 bytes at (FC+0x8) must be a valid size. 

A size is valid if it satisfies two conditions. First, `0x20 <= size < 0x80`. Second, the idx of the size must match the fastbinY idx it came from. The idx of a size is equal to `(size / 0x10) - 2`. For example, `idx(0x20) == 0`, `idx(0x7f) == 5`. More practically, this means that if you set up your fastbin duplicate exploit with chunks of size 0x20, the fake size must be `0x20 <= size < 0x30`. 

Luckily, the fake chunk does not have to be aligned. A good way to keep search for valid chunk sizes is to use `x/40c address` in gdb. This makes it easier to consider the endiness of bytes. Recall that the LSB is on the left, so `0x20 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0` would be a valid header.

---
# Finishing Touches
Once you get malloc to return an arbitrary pointer, you can either read from it to leak the libc base (recall the libc base is randomized everytime because of ASLR), or write to it to get a shell.

Some common exploits are.
- Read from GOT entry
- Write to \_\_malloc\_hook (called whenever malloc is called, usually has a 0x7f size header above it, though it won't be aligned)
- Write to GOT entry
