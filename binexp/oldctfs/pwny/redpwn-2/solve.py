from pwn import *

e = ELF("./chall")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path)

gdb.attach(p)
p.sendlineafter("?", "A" * 0x1000)


p.interactive()
