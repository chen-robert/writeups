from pwn import *

e = ELF("./bezout2shell")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("", )
else:
  p = process(e.path, env={"HOURS_SINCE_START": "1"})
  #, env={"LD_PRELOAD": libc.path})



debug()

p.interactive()
