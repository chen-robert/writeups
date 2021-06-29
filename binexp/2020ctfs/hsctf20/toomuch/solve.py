from pwn import *

p = remote("rev.hsctf.com", 9001)

p.sendlineafter(":", "4294967296 4294967296")

p.interactive()

