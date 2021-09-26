from pwn import *

e = ELF("./word")

p = process(e.path)

gdb.attach(p)

p.interactive()
