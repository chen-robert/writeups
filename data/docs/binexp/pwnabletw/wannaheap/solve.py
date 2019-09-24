from pwn import *

e = ELF("./wannaheap")
libc = ELF("./libc.so")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10308)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

p.sendlineafter(":", str(0x313310))
gdb.attach(p)
p.sendlineafter(":", "1")


p.interactive()
