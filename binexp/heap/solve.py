from pwn import *

e = ELF("./")
libc = ELF("./libc.so.6")

if "--remote" in sys.argv:
  p = remote("", 0)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

def alloc(p):
  p.clean()

def free(p, idx):
  p.clean()



p.interactive()
