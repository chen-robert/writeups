from pwn import *

e = ELF("./")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  s = ssh("2019shell1.picoctf.com", "gamester543", password="")
  p = s.run("")
else:
  p = process(e.path
  #)
  {"LD_PRELOAD": libc.path})


gdb.attach(p)

p.interactive()
