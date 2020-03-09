from pwn import *

e = ELF("./")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path
  #)
  {"LD_PRELOAD": libc.path})


gdb.attach(p)

p.interactive()
