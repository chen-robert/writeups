from pwn import *

p = process("./babylist")

p.sendlineafter(">", "1")
gdb.attach(p)
p.sendlineafter(":", "A" * 0x6f)
p.interactive()
