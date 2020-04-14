from pwn import *

e = ELF("./")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("", )
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})


debug()

p.interactive()
