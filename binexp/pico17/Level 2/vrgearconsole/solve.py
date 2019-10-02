from pwn import *

e = ELF("./vrgearconsole")

if "--remote" in sys.argv:
  p = remote("", 0)
else:
  p = process(e.path)

def alloc(p):
  p.clean()

def free(p, idx):
  p.clean()

p.sendline("admin")
p.sendline("{{ create_long_password() }}")

p.interactive()
