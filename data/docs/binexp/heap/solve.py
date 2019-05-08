from pwn import *

e = ELF("./")
libc = ELF("./libc.so.6")
p = process(e.path, env={"LD_PRELOAD": libc.path})
# p = remote("", )

def alloc(p):
  p.clean()

def free(p, idx):
  p.clean()



p.interactive()
