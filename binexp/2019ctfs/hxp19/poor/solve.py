from pwn import *

e = ELF("./threads")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path)



p.interactive()
